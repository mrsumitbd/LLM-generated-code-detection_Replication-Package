import triton as tl

@tl.jit
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
    # Get the current thread's block index and thread index
    pid = tl.program_id(axis=0)
    num_threads = tl.num_threads()
    
    # Compute the output index
    o_idx = pid * BLOCK_DV
    
    # Load the sequence lengths
    seq_len = B_Seqlens[o_idx // q_heads]
    
    # Compute the start and end indices for the current block
    start = o_idx
    end = min(o_idx + BLOCK_DV, seq_len * q_heads)
    
    # Initialize the output tensor
    output = tl.zeros((end - start, Lv), dtype=tl.float32)
    
    # Iterate over the current block
    for i in tl.arange(start, end):
        # Compute the batch and head indices
        b = i // q_heads
        h = i % q_heads
        
        # Load the corresponding values from Mid_O
        mid_o = Mid_O[b, h, i - b * q_heads * stride_mid_ob]
        
        # Compute the output index
        o_idx = i - start
        
        # Store the output
        output[o_idx] = mid_o
    
    return output