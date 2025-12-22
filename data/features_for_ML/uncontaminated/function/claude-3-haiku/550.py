import torch
import torch.nn.functional as F

def native_sparse_attn_forward(
    q,
    k,
    v,
    kv_block_indices,
    kv_block_mask,
    block_size=128,
    include_block_causal=True,
    return_sliding_window_out=False
):
    batch_size, num_heads, seq_len, head_dim = q.shape
    device = q.device

    # Compute the attention scores
    scores = torch.einsum('bhid,bhjd->bhij', q, k)

    # Apply the block mask
    scores = scores.masked_fill(kv_block_mask.unsqueeze(1), float('-inf'))

    # Apply the causal mask if requested
    if include_block_causal:
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, device=device), diagonal=1).bool()
        causal_mask = causal_mask.unsqueeze(0).unsqueeze(0)
        scores = scores.masked_fill(causal_mask, float('-inf'))

    # Compute the attention weights
    attn_weights = F.softmax(scores, dim=-1)

    # Compute the output
    output = torch.einsum('bhij,bhjd->bhid', attn_weights, v)

    if return_sliding_window_out:
        # Compute the sliding window output
        sliding_window_out = torch.zeros_like(output)
        for i in range(0, seq_len, block_size):
            start = i
            end = min(i + block_size, seq_len)
            sliding_window_out[:, :, start:end] = output[:, :, start:end]
        return output, sliding_window_out
    else:
        return output