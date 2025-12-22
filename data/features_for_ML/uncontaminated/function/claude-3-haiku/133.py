import torch

def sinc(x: torch.Tensor):
    """
    Implementation of sinc, i.e. sin(pi * x) / (pi * x)
    __Warning__: Different to julius.sinc, the input is multiplied by `pi`!
    """
    return torch.where(x == 0, torch.ones_like(x), torch.sin(torch.pi * x) / (torch.pi * x))