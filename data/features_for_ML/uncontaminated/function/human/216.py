import torch
from typing import List, Optional

def add_continuous(
    lhs: torch.Tensor,
    rhs: torch.Tensor,
    out: Optional[torch.Tensor],
    num_ctas=16,
    num_warps=32,
):
    assert lhs.dtype == rhs.dtype and lhs.numel() == rhs.numel()
    if out is None:
        out = torch.empty_like(lhs)
    add_continuous_kernel[(num_ctas, )](  # local memory bw is very high. use many blocks
        lhs, rhs, out, out.numel(), num_warps=num_warps,
        BLOCK_SIZE=num_warps * 32 * 8 * 4,  # per thread has 8*4 elements
    )
    return out