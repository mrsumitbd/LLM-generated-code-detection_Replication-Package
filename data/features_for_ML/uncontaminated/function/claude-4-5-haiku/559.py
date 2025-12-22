def flash_attn_fwd_softmax_lse_correction(
    softmax_lse: torch.Tensor,
    softmax_lse_per_step: torch.Tensor,
):
    """Merge softmax stats of each step in Attention with context parallelism"""
    # softmax_lse shape: (batch_size, num_heads, seq_len_q)
    # softmax_lse_per_step shape: (batch_size, num_heads, seq_len_q, num_steps)
    
    batch_size, num_heads, seq_len_q = softmax_lse.shape
    num_steps = softmax_lse_per_step.shape[-1]
    
    # Reshape softmax_lse_per_step to (batch_size, num_heads, seq_len_q, num_steps)
    lse_per_step = softmax_lse_per_step
    
    # Find the maximum LSE across all steps for numerical stability
    # Shape: (batch_size, num_heads, seq_len_q)
    max_lse = torch.max(lse_per_step, dim=-1)[0]
    
    # Compute the sum of exp(lse_per_step - max_lse) across steps
    # This is equivalent to: sum_i(exp(lse_i - max_lse))
    exp_sum = torch.sum(torch.exp(lse_per_step - max_lse.unsqueeze(-1)), dim=-1)
    
    # Compute the corrected LSE using the log-sum-exp trick
    # lse_corrected = max_lse + log(sum_i(exp(lse_i - max_lse)))
    softmax_lse_corrected = max_lse + torch.log(exp_sum)
    
    return softmax_lse_corrected