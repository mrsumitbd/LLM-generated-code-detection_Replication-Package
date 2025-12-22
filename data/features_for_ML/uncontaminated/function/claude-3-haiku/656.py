import torch
from typing import NamedTuple

class ReduceScatter2DContext(NamedTuple):
    max_M: int
    N: int
    rank: int
    world_size: int
    local_world_size: int
    dtype: torch.dtype
    overlap_with_gemm: bool
    num_reduction_sms: int

def create_reduce_scater_2d_ctx(max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm=True,
                                num_reduction_sms=15) -> ReduceScatter2DContext:
    return ReduceScatter2DContext(
        max_M=max_M,
        N=N,
        rank=rank,
        world_size=world_size,
        local_world_size=local_world_size,
        dtype=dtype,
        overlap_with_gemm=overlap_with_gemm,
        num_reduction_sms=num_reduction_sms
    )