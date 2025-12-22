import torch
import triton

def native_sparse_attn_forward(
    q,
    k,
    v,
    kv_block_indices,
    kv_block_mask,
    block_size = 128,
    include_block_causal = True,
    return_sliding_window_out = False
):
    q, k, v, kv_block_indices = [x if is_contiguous(x) else x.contiguous() for x in (q, k, v, kv_block_indices)]

    batch, nheads, seqlen_q, dim, device = *q.shape, q.device
    _, kv_heads, seqlen_k, _ = k.shape
    assert divisible_by(nheads, kv_heads)
    head_groups = nheads // kv_heads

    assert divisible_by(block_size, 16)

    num_blocks_per_sel = block_size // 16
    num_selected_fine_blocks = kv_block_indices.shape[-1]
    assert kv_block_indices.shape == kv_block_mask.shape

    assert k.shape == (batch, kv_heads, seqlen_k, dim)
    assert v.shape == (batch, kv_heads, seqlen_k, dim)
    assert dim <= 128, "only support head dimensions up to 128"
    assert q.dtype == k.dtype == v.dtype, "All tensors must have the same type"
    assert q.dtype in [torch.float16, torch.bfloat16], "Only support fp16 and bf16"
    assert all([t.is_cuda for t in (q, k, v)])

    softmax_scale = dim ** -0.5

    seqlen_q_rounded = round_up_multiple(seqlen_q, TRITON_BLOCK_SIZE)

    lse = torch.empty((batch, nheads, seqlen_q_rounded), device = device, dtype = torch.float32)
    slide_lse = torch.empty((batch, nheads, seqlen_q_rounded), device = device, dtype = torch.float32)

    o = torch.empty_like(q)
    slide_o = torch.empty_like(q)

    BLOCK_HEADDIM = max(triton.next_power_of_2(dim), 16)
    num_warps = 4 if dim <= 64 else 8

    grid = lambda META: (
        triton.cdiv(seqlen_q, META["BLOCK"]),
        batch * kv_heads,
        (2 if return_sliding_window_out else 1)
    ) # kv heads here, as grouped query heads all loaded, following the paper

    forward_kernel[grid](
        q,
        k,
        v,
        kv_block_indices,
        kv_block_mask,
        o,
        slide_o,
        lse,
        slide_lse,
        softmax_scale,
        q.stride(0),
        q.stride(1),
        q.stride(2),
        k.stride(0),
        k.stride(1),
        k.stride(2),
        v.stride(0),
        v.stride(1),
        v.stride(2),
        o.stride(0),
        o.stride(1),
        o.stride(2),
        kv_block_indices.stride(0),
        kv_block_indices.stride(1),
        kv_block_indices.stride(2),
        lse.stride(0),
        kv_heads,
        seqlen_q,
        seqlen_k,
        seqlen_q_rounded,
        dim,
        seqlen_q // 32,
        seqlen_k // 32,
        BLOCK_HEADDIM,
        BLOCK = 16,
        SEL_BLOCK = block_size,
        QUERY_HEAD_GROUPS = head_groups,
        NUM_SEL_KV_BLOCKS = num_selected_fine_blocks,
        NUM_BLOCKS_PER_SEL = num_blocks_per_sel,
        INCLUDE_BLOCK_CAUSAL = include_block_causal,
        RETURN_SLIDING_OUT = return_sliding_window_out,
        num_warps = num_warps,
        num_stages = 1,
    )

    return o, slide_o, lse, slide_lse