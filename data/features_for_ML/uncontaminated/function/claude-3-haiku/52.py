import torch
from typing import Literal, Optional
from dataclasses import dataclass

@dataclass
class GemmConfig:
    pass

def gemm_act_tuned(
    A: torch.Tensor,
    B: torch.Tensor,
    preact_out: Optional[torch.Tensor],
    postact_out: torch.Tensor,
    C: Optional[torch.Tensor] = None,
    bias: Optional[torch.Tensor] = None,
    activation: Literal[None, "relu", "relu_sq", "gelu_tanh_approx"] = None,
    cu_seqlens_m: Optional[torch.Tensor] = None,
    A_idx: Optional[torch.Tensor] = None,
    dynamic_scheduler: bool = False,
    config: Optional[GemmConfig] = None,
) -> None:
    if activation == "relu":
        postact_out.copy_(torch.maximum(torch.zeros_like(postact_out), postact_out))
    elif activation == "relu_sq":
        postact_out.copy_(torch.square(torch.maximum(torch.zeros_like(postact_out), postact_out)))
    elif activation == "gelu_tanh_approx":
        postact_out.copy_(0.5 * postact_out * (1 + torch.tanh(0.7978845608 * postact_out * (1 + 0.044715 * torch.square(postact_out)))))
    else:
        if C is not None:
            postact_out.copy_(C + postact_out)
        if bias is not None:
            postact_out.add_(bias)