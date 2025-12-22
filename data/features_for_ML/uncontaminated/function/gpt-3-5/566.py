import torch

def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    return torch.where(t > 0, torch.tensor(1), torch.tensor(0))