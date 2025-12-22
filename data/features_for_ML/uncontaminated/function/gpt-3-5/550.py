import torch

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
    assert q.dim() == 3 and k.dim() == 3 and v.dim() == 3
    assert q.size(0) == k.size(0) == v.size(0)
    assert q.size(2) == k.size(2) == v.size(2)
    assert kv_block_indices.dim() == 2
    assert kv_block_indices.size(0) == q.size(0)
    assert kv_block_indices.size(1) == k.size(1)
    assert kv_block_mask.dim() == 2
    assert kv_block_mask.size(0) == q.size(0)
    assert kv_block_mask.size(1) == k.size(1)

    batch_size, num_heads, seq_len_q, head_dim = q.size()
    seq_len_k = k.size(2)
    assert head_dim % num_heads == 0
    head_dim_per_head = head_dim // num_heads

    if include_block_causal:
        assert seq_len_q == seq_len_k

    sliding_window_out = None

    for i in range(batch_size):
        q_i = q[i].view(num_heads, seq_len_q, head_dim_per_head)
        k_i = k[i].view(num_heads, seq_len_k, head_dim_per_head)
        v_i = v[i].view(num_heads, seq_len_k, head_dim_per_head)

        kv_block_indices_i = kv_block_indices[i]
        kv_block_mask_i = kv_block_mask[i]

        attn_weights = torch.einsum('nqd,nkd->nqk', q_i, k_i)
        attn_weights = attn_weights.masked_fill(kv_block_mask_i.unsqueeze(1), float('-inf'))

        attn_weights = torch.nn.functional.softmax(attn_weights, dim=-1)

        if return_sliding_window_out:
            sliding_window_out_i = torch.einsum('nqk,nkd->nqd', attn_weights, v_i)
            if sliding_window_out is None:
                sliding_window_out = sliding_window_out_i.unsqueeze(0)
            else:
                sliding_window_out = torch.cat((sliding_window_out, sliding_window_out_i.unsqueeze(0)), dim=0)

    if return_sliding_window_out:
        return sliding_window_out
    else:
        return torch.einsum('nqk,nkd->nqd', attn_weights, v)