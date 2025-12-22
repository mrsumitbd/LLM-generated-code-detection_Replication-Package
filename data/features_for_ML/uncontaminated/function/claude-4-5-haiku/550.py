def native_sparse_attn_forward(
    q,
    k,
    v,
    kv_block_indices,
    kv_block_mask,
    block_size = 128,
    include_block_causal = False,
    return_sliding_window_out = False
):
    import torch
    import torch.nn.functional as F
    
    batch_size, seq_len, num_heads, head_dim = q.shape
    
    # Reshape for block-wise processing
    num_blocks = (seq_len + block_size - 1) // block_size
    
    # Initialize output
    out = torch.zeros_like(q)
    
    # Process each query block
    for block_idx in range(num_blocks):
        start_idx = block_idx * block_size
        end_idx = min((block_idx + 1) * block_size, seq_len)
        block_len = end_idx - start_idx
        
        q_block = q[:, start_idx:end_idx, :, :]  # (batch, block_size, num_heads, head_dim)
        
        # Get valid KV block indices for this query block
        valid_kv_indices = kv_block_indices[block_idx]
        valid_kv_mask = kv_block_mask[block_idx]
        
        # Collect KV pairs from valid blocks
        kv_list = []
        for kv_idx in valid_kv_indices:
            if kv_idx < 0 or kv_idx >= num_blocks:
                continue
            kv_start = kv_idx * block_size
            kv_end = min((kv_idx + 1) * block_size, seq_len)
            kv_list.append((kv_start, kv_end, kv_idx))
        
        if not kv_list:
            continue
        
        # Concatenate all KV blocks
        k_blocks = []
        v_blocks = []
        for kv_start, kv_end, kv_idx in kv_list:
            k_blocks.append(k[:, kv_start:kv_end, :, :])
            v_blocks.append(v[:, kv_start:kv_end, :, :])
        
        k_concat = torch.cat(k_blocks, dim=1)  # (batch, total_kv_len, num_heads, head_dim)
        v_concat = torch.cat(v_blocks, dim=1)
        
        # Compute attention scores
        # q_block: (batch, block_len, num_heads, head_dim)
        # k_concat: (batch, total_kv_len, num_heads, head_dim)
        
        q_block = q_block.transpose(1, 2)  # (batch, num_heads, block_len, head_dim)
        k_concat = k_concat.transpose(1, 2)  # (batch, num_heads, total_kv_len, head_dim)
        v_concat = v_concat.transpose(1, 2)  # (batch, num_heads, total_kv_len, head_dim)
        
        scores = torch.matmul(q_block, k_concat.transpose(-2, -1))  # (batch, num_heads, block_len, total_kv_len)
        scores = scores / (head_dim ** 0.5)
        
        # Apply causal mask if needed
        if include_block_causal:
            causal_mask = torch.triu(torch.ones(block_len, k_concat.shape[-2], device=q.device, dtype=torch.bool), diagonal=1)
            scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float('-inf'))
        
        # Apply softmax
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = torch.nan_to_num(attn_weights, 0.0)
        
        # Apply attention to values
        attn_out = torch.matmul(attn_weights, v_concat)  # (batch, num_heads, block_len, head_dim)
        attn_out = attn_out.transpose(1, 2)  # (batch, block_len, num_heads, head_dim)
        
        out[:, start_idx:end_idx, :, :] = attn_out
    
    if return_sliding_window_out:
        return out, None
    
    return out