import torch

def sinc(x: torch.Tensor):
    """
    Implementation of sinc, i.e. sin(pi * x) / (pi * x)
    __Warning__: Different to julius.sinc, the input is multiplied by `pi`!
    """
    pi = torch.pi
    # Compute sin(pi * x) / (pi * x)
    y = torch.sin(pi * x) / (pi * x)
    # Handle the singularity at x == 0
    # Use a mask to replace NaNs/inf with 1.0
    zero_mask = x == 0
    if zero_mask.any():
        y = torch.where(zero_mask, torch.ones_like(x), y)
    return y