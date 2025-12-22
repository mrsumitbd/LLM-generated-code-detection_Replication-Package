import torch

def mask_to_bias(mask: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    return (~mask).to(dtype)