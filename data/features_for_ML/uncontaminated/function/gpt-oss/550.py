import torch
import math

def native_sparse_attn_forward(
    q,
    k,
    v,
    kv_block_indices,
    kv_block_mask,
    block_size=128,
    include_block_causal=True,
    return_sliding_window_out=False,
):
    """
    Sparse attention with block‑wise KV gathering.

    Parameters
    ----------
    q, k, v : torch.Tensor
        Query, key and value tensors of shape
        (batch, heads, seq_len, head_dim).
    kv_block_indices : torch.LongTensor
        Indices of KV blocks to attend to for each query.
        Shape: (batch, heads, seq_len, num_blocks_per_query).
    kv_block_mask : torch.BoolTensor
        Mask indicating which KV blocks are valid.
        Shape: (batch, heads, seq_len, num_blocks_per_query).
    block_size : int
        Size of each KV block.
    include_block_causal : bool
        If True, apply causal masking within each block.
    return_sliding_window_out : bool
        If True, return the attention weights as well.

    Returns
    -------
    out : torch.Tensor
        Attention output of shape (batch, heads, seq_len, head_dim).
    (optional) attn_weights : torch.Tensor
        Attention weights of shape
        (batch, heads, seq_len, seq_kv).
    """
    # Basic shapes
    B, H, L, D = q.shape
    _, _, K, _ = k.shape
    num_kv_blocks = K // block_size
    num_blocks_per_query = kv_block_indices.shape[-1]

    # Reshape KV into blocks
    k_blocks = k.view(B, H, num_kv_blocks, block_size, D)
    v_blocks = v.view(B, H, num_kv_blocks, block_size, D)

    # Gather the requested blocks for each query
    # kv_block_indices: (B, H, L, num_blocks_per_query)
    # Expand to gather block_size and head_dim
    idx_exp = kv_block_indices.unsqueeze(-1).unsqueeze(-1)  # (B,H,L,nb,1,1)
    idx_exp = idx_exp.expand(-1, -1, -1, -1, block_size, D)

    # Gather keys and values
    k_gathered = torch.gather(k_blocks, 2, idx_exp)  # (B,H,L,nb,block_size,D)
    v_gathered = torch.gather(v_blocks, 2, idx_exp)

    # Flatten blocks and block_size into a single KV dimension
    seq_kv = num_blocks_per_query * block_size
    k_flat = k_gathered.reshape(B, H, L, seq_kv, D)
    v_flat = v_gathered.reshape(B, H, L, seq_kv, D)

    # Compute attention scores
    # q: (B,H,L,D) -> (B,H,L,1,D)
    # k_flat: (B,H,L,seq_kv,D)
    scores = torch.matmul(q.unsqueeze(3), k_flat.transpose(-1, -2)).squeeze(3)  # (B,H,L,seq_kv)
    scores = scores / math.sqrt(D)

    # Apply KV mask
    # kv_block_mask: (B,H,L,nb) -> expand to seq_kv
    mask_exp = kv_block_mask.unsqueeze(-1).expand(-1, -1, -1, -1, block_size)
    mask_flat = mask_exp.reshape(B, H, L, seq_kv)
    scores = scores.masked_fill(~mask_flat, float("-inf"))

    # Optional causal mask within each block
    if include_block_causal:
        # Create a causal mask for a single block
        causal_block = torch.tril(torch.ones(block_size, block_size, device=scores.device))
        # Expand to all blocks
        causal_mask = causal_block.repeat(num_blocks_per_query, 1)  # (seq_kv, block_size)
        # For each query position, we need to offset the mask according to the block start
        # Here we assume blocks are contiguous and aligned with query positions.
        # This is a simplified implementation that may not be fully correct for arbitrary block layouts.
        # We broadcast the mask across batch, heads, seq_len.
        causal_mask = causal_mask.unsqueeze(0).unsqueeze(0).unsqueeze(0)  # (1,1,1,seq_kv,block_size)
        # We need to mask positions where kv_pos > q_pos within each block.
        # Compute relative positions
        kv_pos = torch.arange(seq_kv, device=scores.device).view(1,1,1,seq_kv)
        q_pos = torch.arange(L, device=scores.device).view(1,1,L,1)
        # For each block, the start position is block_index * block_size
        block_start = torch.arange(num_blocks_per_query, device=scores.device).view(1,1,1,1,1) * block_size
        kv_rel_pos = kv_pos - block_start  # (1,1,1,seq_kv,1)
        q_rel_pos = q_pos  # (1,1,L,1)
        # Mask where kv_rel_pos > q_rel_pos
        causal_mask = (kv_rel_pos <= q_rel_pos).squeeze(-1)  # (1,1,L,seq_kv)
        scores = scores.masked_fill(~causal_mask, float("-inf"))

    # Softmax
    attn_weights = torch.softmax(scores, dim=-1)

    # Weighted sum of values
    out = torch.matmul(attn_weights.unsqueeze(-2), v_flat).squeeze(-2)  # (B,H,L,D)

    if return_sliding_window_out:
        return out, attn_weights
    return out