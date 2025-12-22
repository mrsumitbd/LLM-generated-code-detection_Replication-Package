from typing import Any, overload
import torch
from magi_attention.utils import nvtx, wrap_to_list
import torch.distributed as dist
from ...work import GeneralWork, WorkWithPostProcessFn
from ._buffer import GrpCollBuffer
from ._config import GrpCollConfig
from ._handle import GrpCollHandle
from ._mgr import grpcoll_mgr
from .utils import (
    get_a2av_perm_idxs_from_group_cast_meta,
    get_group_reduce_handle_from_sym_group_cast,
    get_native_group_cast_meta,
    maybe_lazy_init_buffer,
)

def native_group_cast_impl(
    input: torch.Tensor,
    output: torch.Tensor | None,
    input_split_sizes: list[int] | torch.Tensor,
    output_split_sizes: list[int] | torch.Tensor,
    dst_indices: list[list[int]] | torch.Tensor,
    src_index: list[int] | torch.Tensor,
    group: dist.ProcessGroup,
    async_op: bool = False,
    cast_lse: bool = False,
    input_lse: torch.Tensor | None = None,
    output_lse: torch.Tensor | None = None,
    **kwargs,
) -> WorkWithPostProcessFn:
    """Native group-cast implementation"""
    # maybe lazy init buffer
    maybe_lazy_init_buffer(group)

    # get grpcoll config and buffer
    config: GrpCollConfig = grpcoll_mgr.get_config(group)
    buffer: GrpCollBuffer = grpcoll_mgr.get_buffer(group)
    assert config is not None and buffer is not None

    # pack input and output
    input: list[torch.Tensor] = wrap_to_list(input)
    output: list[torch.Tensor] | None = (
        wrap_to_list(output) if output is not None else output
    )
    num_groups = len(input)

    # get meta dict and handle
    input_seqlen: int = input[0].size(0)
    output_seqlen: int | None = (
        output[0].size(0) if output is not None else kwargs.pop("output_seqlen", None)
    )
    meta_dict: dict[str, Any] = kwargs.pop("native_group_cast_meta_dict", {})
    handle_dict: dict[str, GrpCollHandle] = kwargs.pop("native_grpcoll_handle_dict", {})
    handle: GrpCollHandle | None = handle_dict.get("group_cast", None)

    # transfer group-cast meta args to dispatch meta args
    if meta_dict:
        num_tokens_per_rank = meta_dict["num_tokens_per_rank"]
        num_tokens_per_rdma_rank = meta_dict["num_tokens_per_rdma_rank"]
        is_token_in_rank = meta_dict["is_token_in_rank"]
        post_perm_idx = meta_dict["post_perm_idx"]
    else:
        (
            num_tokens_per_rank,
            num_tokens_per_rdma_rank,
            is_token_in_rank,
        ) = get_native_group_cast_meta(
            input_split_sizes=input_split_sizes,
            dst_indices=dst_indices,
            group=group,
            input_seqlen=input_seqlen,
            # HACK: leave a slot for t2r_idx
            # since for now, we transfer the group_cast meta to it inside anyway
            # which is helpful in the token-level communication scenarios such as ep, nsa
            t2r_idx=kwargs.pop("t2r_idx", None),
        )

        # for group-cast, perm_to_a2av_idx is the post_perm_idx
        post_perm_idx = get_a2av_perm_idxs_from_group_cast_meta(
            output_split_sizes=output_split_sizes,
            src_index=src_index,
            num_ranks=group.size(),
            output_seqlen=output_seqlen,
        )

    # launch dispatch kernel
    (
        recv_x,
        recv_lse,
        handle,
        event,
    ) = buffer.group_cast(
        x=input,
        recv_x=output,
        handle=handle,
        num_tokens_per_rank=num_tokens_per_rank,
        num_tokens_per_rdma_rank=num_tokens_per_rdma_rank,
        is_token_in_rank=is_token_in_rank,
        post_perm_idx=post_perm_idx,
        config=config,
        previous_event=None,
        async_op=async_op,
        allocate_on_comm_stream=False,
        cast_lse=cast_lse,
        lse=input_lse,
        recv_lse=output_lse,
    )

    # unpack recv_x
    if num_groups == 1:
        recv_x = recv_x[0]

    # HACK: prepare handle for symmetric group-reduce or cached group-cast
    handle_dict["group_cast"] = handle
    handle_dict["group_reduce"] = handle

    # prepare work with post-process
    work_with_post_process_fn = WorkWithPostProcessFn(
        work=GeneralWork(event),
        post_process_fn=(
            (lambda *args, **kwargs: (recv_x, recv_lse))
            if cast_lse
            else lambda *args, **kwargs: recv_x
        ),
        async_op=async_op,
    )

    return work_with_post_process_fn