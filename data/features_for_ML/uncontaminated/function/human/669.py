from magi_attention.common import AttnRanges
from magi_attention.config import (
    DispatchConfig,
    DistAttnConfig,
    GrpCollConfig,
    OverlapConfig,
)
import torch.distributed as dist
from magi_attention.common.enum import AttnMaskType, AttnRole
from torch.distributed.device_mesh import DeviceMesh
import magi_attention

def init_dist_attn_runtime_key(
    q_ranges: AttnRanges,
    k_ranges: AttnRanges,
    attn_mask_type: list[AttnMaskType],
    total_seqlen_q: int,
    total_seqlen_k: int,
    pad_size: int,
    chunk_size: int,
    cp_group: dist.ProcessGroup,
    cp_mesh: DeviceMesh | None,
    dist_attn_config: DistAttnConfig,
) -> DistAttnRuntimeKey:
    return DistAttnRuntimeKey(
        q_ranges=q_ranges,
        k_ranges=k_ranges,
        attn_mask_type=tuple(attn_mask_type),
        total_seqlen_q=total_seqlen_q,
        total_seqlen_k=total_seqlen_k,
        pad_size=pad_size,
        chunk_size=chunk_size,
        cp_group=cp_group,
        cp_mesh=cp_mesh,
        dist_attn_config=dist_attn_config,
        # auto set other flags that might influence the runtime behavior
        is_deterministic_mode_enable=magi_attention.is_deterministic_mode_enable(),
        is_hierarchical_comm_enable=magi_attention.comm.is_hierarchical_comm_enable(),
        is_qo_comm_enable=magi_attention.comm.is_qo_comm_enable(),
        is_native_grpcoll_enable=magi_attention.comm.is_native_grpcoll_enable(),
    )