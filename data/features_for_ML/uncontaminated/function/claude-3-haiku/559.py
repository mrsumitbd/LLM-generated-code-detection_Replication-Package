def flash_attn_fwd_softmax_lse_correction(
    softmax_lse: torch.Tensor,
    softmax_lse_per_step: torch.Tensor,
):
    """Merge softmax stats of each step in Attention with context parallelism"""
    softmax_lse_correction = softmax_lse - torch.logsumexp(softmax_lse_per_step, dim=1, keepdim=True)
    return softmax_lse_correction