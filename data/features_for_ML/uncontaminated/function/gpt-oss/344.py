import torch

def sdpa_bwd_preprocess(
    do: torch.Tensor,
    o: torch.Tensor,
) -> torch.Tensor:
    """
    Preprocess the gradients for the backward pass of scaled dot-product attention.

    Parameters
    ----------
    do : torch.Tensor
        Gradient of the loss with respect to the attention output.
        Expected shape: [b, nh, sq, se].
    o : torch.Tensor
        Attention output tensor.
        Expected shape: [b, nh, sq, se].

    Returns
    -------
    torch.Tensor
        The element‑wise product of `do` and `o`, summed over the last dimension
        (the sequence length of the values). The resulting shape is
        [b, nh, sq, 1].
    """
    # Element‑wise product followed by a sum over the last dimension.
    return torch.sum(do * o, dim=-1, keepdim=True)