import torch

def sinc(x: torch.Tensor):
    eps = 1e-8
    return torch.where(torch.abs(x) < eps, torch.ones_like(x), torch.sin(torch.pi * x) / (torch.pi * x))