def _hacked_flash_attention_forward(*args, **kwargs):
    """
    Hacked version of flash attention forward that handles edge cases and provides
    a fallback implementation when needed.
    """
    import torch
    from torch import nn
    
    # Extract arguments - typically (self, q, k, v, causal, q_bucket_size, k_bucket_size)
    if len(args) >= 4:
        self_obj = args[0]
        q = args[1]
        k = args[2]
        v = args[3]
        causal = args[4] if len(args) > 4 else kwargs.get('causal', False)
        q_bucket_size = args[5] if len(args) > 5 else kwargs.get('q_bucket_size', 512)
        k_bucket_size = args[6] if len(args) > 6 else kwargs.get('k_bucket_size', 512)
    else:
        raise ValueError("Insufficient arguments for flash attention forward")
    
    # Handle edge case: if any input is empty
    if q.numel() == 0 or k.numel() == 0 or v.numel() == 0:
        return torch.zeros_like(q)
    
    # Get dimensions
    batch_size, seq_len_q, num_heads, head_dim = q.shape
    _, seq_len_k, _, _ = k.shape
    
    # Reshape for attention computation
    q_reshaped = q.view(batch_size * num_heads, seq_len_q, head_dim)
    k_reshaped = k.view(batch_size * num_heads, seq_len_k, head_dim)
    v_reshaped = v.view(batch_size * num_heads, seq_len_k, head_dim)
    
    # Compute attention scores
    scores = torch.matmul(q_reshaped, k_reshaped.transpose(-2, -1)) / (head_dim ** 0.5)
    
    # Apply causal mask if needed
    if causal:
        causal_mask = torch.triu(torch.ones(seq_len_q, seq_len_k, device=q.device, dtype=torch.bool), diagonal=seq_len_k - seq_len_q + 1)
        scores = scores.masked_fill(~causal_mask, float('-inf'))
    
    # Apply softmax
    attn_weights = torch.softmax(scores, dim=-1)
    
    # Handle NaN values from softmax on -inf
    attn_weights = torch.nan_to_num(attn_weights, 0.0)
    
    # Apply attention to values
    output = torch.matmul(attn_weights, v_reshaped)
    
    # Reshape back to original format
    output = output.view(batch_size, seq_len_q, num_heads, head_dim)
    
    return output