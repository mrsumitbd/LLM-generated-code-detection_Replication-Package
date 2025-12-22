import torch
from torch import Tensor
from typing import Optional, Literal

# Simple GemmConfig placeholder (unused in this implementation)
class GemmConfig:
    pass

def gemm_act_tuned(
    # (M, K) or (L, M, K) or (total_M, K) if varlen_m or (whatever, K) if gather_A with varlen_m
    A: Tensor,
    B: Tensor,  # (K, N) or (L, K, N)
    # (M, N) or (L, M, N) or (total_M, N) if varlen_m - None if not storing preact
    preact_out: Optional[Tensor],
    postact_out: Tensor,  # (M, N) or (L, M, N) or (total_M, N) if varlen_m
    C: Optional[Tensor] = None,  # (M, N) or (L, M, N) or (total_M, N) if varlen_m
    bias: Optional[Tensor] = None,  # (N,) or (L, N)
    activation: Literal[None, "relu", "relu_sq", "gelu_tanh_approx"] = None,
    cu_seqlens_m: Optional[Tensor] = None,  # (L+1), int32
    A_idx: Optional[Tensor] = None,  # (total_M,) if gather_A with varlen_m
    dynamic_scheduler: bool = False,
    config: Optional[GemmConfig] = None,
) -> None:
    """
    A lightweight, pure‑torch implementation of a tuned GEMM + activation routine.
    The function supports batched (L, M, K) × (L, K, N) multiplication, optional
    bias addition, optional pre‑activation output, and a few activation functions.
    """
    # ------------------------------------------------------------------
    # 1. Handle gather_A (if A_idx is provided)
    # ------------------------------------------------------------------
    if A_idx is not None:
        # A_idx is a 1‑D index tensor selecting rows from A
        # We assume A is 2‑D (M, K) or 3‑D (L, M, K) and gather along the first dimension
        if A.dim() == 2:
            A = A[A_idx]
        elif A.dim() == 3:
            # Gather along the second dimension (M)
            # A_idx shape: (total_M,) where total_M = sum of lengths per batch
            # We need to reshape A_idx into (L, M) where M is the original M
            # For simplicity, we broadcast A_idx to match A's shape
            # This is a best‑effort implementation; real gather logic may differ
            A = torch.index_select(A, 1, A_idx)
        else:
            raise ValueError(f"Unsupported A dimension {A.dim()} for gather_A")

    # ------------------------------------------------------------------
    # 2. Prepare batched or unbatched multiplication
    # ------------------------------------------------------------------
    # Determine if we are in batched mode
    batched = B.dim() == 3

    if batched:
        # B shape: (L, K, N)
        L, K, N = B.shape
        if A.dim() == 2:
            # Broadcast A to (L, M, K)
            A = A.unsqueeze(0).expand(L, -1, -1)
        elif A.dim() == 3:
            if A.shape[0] != L:
                raise ValueError("Batch dimension of A and B must match")
        else:
            raise ValueError(f"Unsupported A dimension {A.dim()} for batched GEMM")

        # Perform batched matmul
        mat = torch.bmm(A, B)  # (L, M, N)
    else:
        # Unbatched GEMM
        mat = torch.matmul(A, B)  # (M, N)

    # ------------------------------------------------------------------
    # 3. Add bias and C if provided
    # ------------------------------------------------------------------
    if C is not None:
        mat = mat + C

    if bias is not None:
        # bias shape: (N,) or (L, N)
        mat = mat + bias

    # ------------------------------------------------------------------
    # 4. Store pre‑activation output if requested
    # ------------------------------------------------------------------
    if preact_out is not None:
        preact_out.copy_(mat)

    # ------------------------------------------------------------------
    # 5. Apply activation function
    # ------------------------------------------------------------------
    if activation is not None:
        if activation == "relu":
            mat = torch.relu(mat)
        elif activation == "relu_sq":
            mat = torch.relu(mat) ** 2
        elif activation == "gelu_tanh_approx":
            # Approximate GELU: 0.5 * x * (1 + tanh(sqrt(2/pi)*(x + 0.044715*x^3)))
            sqrt_2_over_pi = torch.sqrt(torch.tensor(2.0 / torch.pi, dtype=mat.dtype, device=mat.device))
            inner = sqrt_2_over_pi * (mat + 0.044715 * mat ** 3)
            mat = 0.5 * mat * (1 + torch.tanh(inner))
        else:
            raise ValueError(f"Unsupported activation: {activation}")

    # ------------------------------------------------------------------
    # 6. Write the final result to postact_out
    # ------------------------------------------------------------------
    postact_out.copy_(mat)