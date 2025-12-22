import torch

def flash_attn_fwd_softmax_lse_correction(
    softmax_lse: torch.Tensor,
    softmax_lse_per_step: torch.Tensor,
):
    """
    Merge softmax statistics of each step in Attention with context parallelism.

    Parameters
    ----------
    softmax_lse : torch.Tensor
        The log‑sum‑exp of the softmax over all steps for each query.
        Expected shape: [B, H, L] where
        B = batch size, H = number of heads, L = sequence length.
    softmax_lse_per_step : torch.Tensor
        The log‑sum‑exp of the softmax for each individual step.
        Expected shape: [B, H, L, S] where S is the number of steps.

    Returns
    -------
    torch.Tensor
        The corrected log‑sum‑exp for each query after merging all steps.
        Shape: [B, H, L]
    """
    # If the per‑step tensor has the same number of dimensions as the base LSE,
    # we assume it already contains the merged value and simply return it.
    if softmax_lse_per_step.dim() == softmax_lse.dim():
        return softmax_lse_per_step

    # Broadcast the base LSE to match the per‑step tensor shape.
    # This allows us to compute the difference for each step.
    diff = softmax_lse_per_step - softmax_lse.unsqueeze(-1)

    # Compute the log‑sum‑exp over the step dimension.
    # The result has the same shape as the base LSE.
    lse_corr = softmax_lse + torch.logsumexp(diff, dim=-1)

    return lse_corr