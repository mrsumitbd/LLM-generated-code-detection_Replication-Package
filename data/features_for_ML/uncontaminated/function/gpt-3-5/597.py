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
    for b in range(batch):
        for l in range(Lv):
            for h in range(q_heads):
                for i in range(B_Seqlens[b]):
                    for j in range(BLOCK_DV):
                        for k in range(NUM_KV_SPLITS):
                            Mid_O[b, l, h, i * stride_mid_ob + j * stride_mid_oh + k * stride_mid_os] += o[b, l, h, i * stride_obs + j * stride_oh + k]