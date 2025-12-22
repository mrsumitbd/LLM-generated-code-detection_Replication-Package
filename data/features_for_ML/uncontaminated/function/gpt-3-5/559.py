def flash_attn_fwd_softmax_lse_correction(softmax_lse, softmax_lse_per_step):
    return softmax_lse + softmax_lse_per_step - softmax_lse_per_step.mean(dim=-1, keepdim=True)