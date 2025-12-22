import triton
import triton.language as tl

def kernel_inter_rank_gqa_fwd_batch_decode_combine_kv(
    Mid_O,
    o,
    B_Seqlens,
    batch,
    q_heads,
    stride_mid_ob,
    stride_mid_oh,
    stride_mid_os,
    stride_obs,
    stride_oh,
    NUM_KV_SPLITS: tl.constexpr,
    BLOCK_DV: tl.constexpr,
    Lv: tl.constexpr,
):
    # Compute program id and decompose it into batch, head, and split indices
    pid = tl.program_id(0)
    batch_idx = pid // (q_heads * NUM_KV_SPLITS)
    head_idx = (pid // NUM_KV_SPLITS) % q_heads
    split_idx = pid % NUM_KV_SPLITS

    # Load the sequence length for this batch
    seq_len = tl.load(B_Seqlens + batch_idx)

    # Compute the offset for the current block
    offset = tl.arange(0, BLOCK_DV)
    mask = offset < seq_len

    # Compute the base addresses for Mid_O and o
    mid_base = batch_idx * stride_mid_ob + head_idx * stride_mid_oh + split_idx * stride_mid_os
    o_base   = batch_idx * stride_obs + head_idx * stride_oh

    # Load the values from Mid_O and o, applying the mask
    mid_vals = tl.load(Mid_O + mid_base + offset, mask=mask, other=0)
    o_vals   = tl.load(o + o_base + offset, mask=mask, other=0)

    # Combine the KV values (here we simply add them)
    o_vals = o_vals + mid_vals

    # Store the combined result back to o
    tl.store(o + o_base + offset, o_vals, mask=mask)