import torch
from typing import Optional

def add_continuous(
    lhs: torch.Tensor,
    rhs: torch.Tensor,
    out: Optional[torch.Tensor],
    num_ctas=16,
    num_warps=32,
):
    if out is None:
        out = torch.empty_like(lhs)
    
    num_elements = lhs.numel()
    block_size = num_ctas * num_warps * 32
    grid_size = (num_elements + block_size - 1) // block_size
    
    add_continuous_kernel[grid_size, block_size](lhs, rhs, out)
    
    return out

def add_continuous_kernel(lhs, rhs, out):
    idx = torch.distributed.get_global_rank()
    stride = torch.distributed.get_world_size()
    
    for i in range(idx, lhs.numel(), stride):
        out[i] = lhs[i] + rhs[i]