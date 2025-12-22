import torch

def sinc(x: torch.Tensor):
    """
    Implementation of sinc, i.e. sin(pi * x) / (pi * x)
    __Warning__: Different to julius.sinc, the input is multiplied by `pi`!
    """
    x_pi = x * torch.pi
    result = torch.where(x_pi == 0, torch.ones_like(x_pi), torch.sin(x_pi) / x_pi)
    return result