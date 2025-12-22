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

    block = (num_warps, 1, 1)
    grid = (num_ctas, 1, 1)

    add_continuous_kernel[grid, block](lhs, rhs, out)

    return out

@torch.cuda.kernel_func
def add_continuous_kernel(
    lhs: torch.Tensor,
    rhs: torch.Tensor,
    out: torch.Tensor,
):
    i = torch.cuda.grid(1)
    if i < lhs.numel():
        out[i] = lhs[i] + rhs[i]