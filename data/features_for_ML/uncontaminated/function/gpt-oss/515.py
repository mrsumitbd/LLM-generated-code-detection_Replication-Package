import torch
import math

def sinc(x: torch.Tensor):
    """
    Implementation of sinc, i.e. sin(pi * x) / (pi * x)
    __Warning__: Different to julius.sinc, the input is multiplied by `pi`!
    """
    pi = torch.tensor(math.pi, dtype=x.dtype, device=x.device)
    denom = pi * x
    one = torch.tensor(1.0, dtype=x.dtype, device=x.device)
    return torch.where(denom == 0, one, torch.sin(denom) / denom)