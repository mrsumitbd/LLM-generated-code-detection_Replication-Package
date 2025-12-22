from typing import Optional, Literal

def gemm_act_tuned(
    A: Tensor,
    B: Tensor,
    preact_out: Optional[Tensor],
    postact_out: Tensor,
    C: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    activation: Literal[None, "relu", "relu_sq", "gelu_tanh_approx"] = None,
    cu_seqlens_m: Optional[Tensor] = None,
    A_idx: Optional[Tensor] = None,
    dynamic_scheduler: bool = False,
    config: Optional[GemmConfig] = None,
) -> None:
    pass