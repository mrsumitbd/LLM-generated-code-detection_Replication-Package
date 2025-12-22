import torch
from typing import Union

def _lerp(
    a: Union[torch.Tensor, float, int], b: Union[torch.Tensor, float, int], t: float
) -> Union[torch.Tensor, float, int]:
    if isinstance(a, torch.Tensor):
        return a + t * (b - a)
    elif isinstance(a, (float, int)):
        return a + t * (b - a)
    else:
        raise TypeError("Input types not supported for linear interpolation")