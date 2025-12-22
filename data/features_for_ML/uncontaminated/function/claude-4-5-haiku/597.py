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
    pid_b = tl.program_id(0)
    pid_h = tl.program_id(1)
    pid_s = tl.program_id(2)
    
    # Get sequence length for this batch
    seqlen = tl.load(B_Seqlens + pid_b)
    
    # Compute offsets
    offs_v = tl.arange(0, BLOCK_DV)
    
    # Initialize accumulator for combining splits
    acc_o = tl.zeros((BLOCK_DV,), dtype=tl.float32)
    acc_m = tl.zeros((1,), dtype=tl.float32)
    acc_l = tl.zeros((1,), dtype=tl.float32)
    
    # Iterate over KV splits
    for split_idx in range(NUM_KV_SPLITS):
        # Load intermediate results from Mid_O
        mid_o_offset = (
            pid_b * stride_mid_ob +
            pid_h * stride_mid_oh +
            split_idx * stride_mid_os +
            offs_v
        )
        
        mid_o_val = tl.load(Mid_O + mid_o_offset, mask=offs_v < BLOCK_DV, other=0.0)
        
        # Accumulate
        acc_o += mid_o_val
    
    # Store final output
    o_offset = (
        pid_b * stride_obs +
        pid_h * stride_oh +
        offs_v
    )
    
    tl.store(o + o_offset, acc_o, mask=offs_v < BLOCK_DV)