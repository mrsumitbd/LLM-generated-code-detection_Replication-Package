import torch

def sdpa_bwd_preprocess(do: torch.Tensor, o: torch.Tensor) -> torch.Tensor:
    return do + o