def sdpa_bwd_preprocess(
    do: torch.Tensor,
    o: torch.Tensor,
) -> torch.Tensor:
    # shape: [b, nh, sq, 1]
    return (do * o).sum(dim=-1, keepdim=True)