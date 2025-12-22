import torch

def sdpa_bwd_preprocess(
    do: torch.Tensor,
    o: torch.Tensor,
) -> torch.Tensor:
    # shape: [b, nh, sq, 1]
    delta = (do * o).sum(-1, keepdim=True)
    return delta