import torch
import torch.nn.functional as F

def gelu_and_mul_cuda(x: torch.Tensor) -> torch.Tensor:
    """
    Apply GELU to the second half of the last dimension of `x` and multiply it element‑wise
    with the first half.

    Parameters
    ----------
    x : torch.Tensor
        Input tensor. Must have at least one dimension.

    Returns
    -------
    torch.Tensor
        Tensor of the same shape as `x` where the last dimension has been processed
        as described.
    """
    # Ensure we are on a CUDA device if available
    device = x.device

    # Compute split index
    d = x.shape[-1] // 2

    # Slice the tensor into two halves
    first_half = x[..., :d]
    second_half = x[..., d:]

    # Apply GELU to the second half
    gelu_second = F.gelu(second_half)

    # Element‑wise multiplication
    result = first_half * gelu_second

    return result