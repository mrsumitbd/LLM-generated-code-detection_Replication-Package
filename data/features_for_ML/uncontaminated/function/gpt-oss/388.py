import torch
import torch.distributed as dist
from typing import List, Union, Optional, Any

# Try to import WorkWithPostProcessFn; if not available, define a minimal stub.
try:
    from .work import WorkWithPostProcessFn  # type: ignore
except Exception:
    class WorkWithPostProcessFn:
        def __init__(self, work: Optional[Any], post_process_fn: Optional[Any]) -> None:
            self.work = work
            self.post_process_fn = post_process_fn


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

    # Normalize split sizes to Python lists
    if isinstance(input_split_sizes, torch.Tensor):
        input_split_sizes = input_split_sizes.tolist()
    if isinstance(output_split_sizes, torch.Tensor):
        output_split_sizes = output_split_sizes.tolist()

    # Determine group size
    world_size = dist.get_world_size(group)

    # Build scatter list from input tensor
    scatter_list: List[torch.Tensor] = []
    offset = 0
    for i in range(world_size):
        sz = input_split_sizes[i] if i < len(input_split_sizes) else 0
        if sz > 0:
            # Use .narrow to avoid copying the whole tensor
            slice_tensor = input.narrow(0, offset, sz).clone()
        else:
            slice_tensor = torch.empty(0, dtype=input.dtype, device=input.device)
        scatter_list.append(slice_tensor)
        offset += sz

    # Prepare output tensor if not provided
    if output is None:
        total_out = sum(output_split_sizes) if output_split_sizes else input.numel()
        output = torch.empty(total_out, dtype=input.dtype, device=input.device)

    # Resolve source rank
    if isinstance(src_index, (list, torch.Tensor)):
        src = src_index[0] if isinstance(src_index, list) else src_index.item()
    else:
        src = src_index

    # Perform scatter (async or sync)
    if async_op:
        work = dist.scatter(
            output,
            scatter_list,
            src=src,
            group=group,
            async_op=True,
        )
    else:
        dist.scatter(
            output,
            scatter_list,
            src=src,
            group=group,
            async_op=False,
        )
        work = None

    # Post‑process function (e.g., copy LSE tensors)
    def post_process() -> None:
        if cast_lse and input_lse is not None and output_lse is not None:
            output_lse.copy_(input_lse)

    return WorkWithPostProcessFn(work, post_process)