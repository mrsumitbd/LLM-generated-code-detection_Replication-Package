from typing import Callable, Iterator, List, Union
import torch

def _lerp(
    a: Union[torch.Tensor, float, int], b: Union[torch.Tensor, float, int], t: float
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
    return a * (1 - t) + b * t