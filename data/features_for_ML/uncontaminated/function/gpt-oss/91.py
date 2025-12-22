import torch
from typing import Union

def _lerp(
    a: Union[torch.Tensor, float, int],
    b: Union[torch.Tensor, float, int],
    t: float
) -> Union[torch.Tensor, float, int]:
    """Computes LERP, the Linear Interpolation function between two tensors, a and b.

    Args:
        a (torch.Tensor, float, int): Start tensor of arbitrary shape.
        b (torch.Tensor, float, int): End tensor, of similar shape to a.
        t (float): interpolation factor, a scalar between 0 and 1 that determines where the result lies on the
            interpolation curve.

    Returns:
        torch.Tensor: Interpolated tensor, same shape as a and b.
    """
    # If both are torch tensors, use torch.lerp
    if isinstance(a, torch.Tensor) and isinstance(b, torch.Tensor):
        return torch.lerp(a, b, t)

    # If one is a tensor and the other is a scalar, broadcast the scalar
    if isinstance(a, torch.Tensor) and not isinstance(b, torch.Tensor):
        b_tensor = torch.full_like(a, b)
        return torch.lerp(a, b_tensor, t)

    if isinstance(b, torch.Tensor) and not isinstance(a, torch.Tensor):
        a_tensor = torch.full_like(b, a)
        return torch.lerp(a_tensor, b, t)

    # Both are scalars (int or float)
    return a + t * (b - a)