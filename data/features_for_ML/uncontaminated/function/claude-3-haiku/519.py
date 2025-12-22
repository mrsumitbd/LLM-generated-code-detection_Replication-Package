def kernel_all2all_pull_intra_node_nvl(
    gemm_out_ptr,
    gemm_barrier_ptr,
    cum_seqlen_cpu_tuple,
    cum_seqlen_gpu_ptr,
    q_out_ptr,
    k_out_ptr,
    v_out_ptr,
    sp_size: tl.constexpr,
    rank,
    sp_rank,
    qkv_out_features: tl.constexpr,
    head_dim: tl.constexpr,
    gqa: tl.constexpr,
    BLOCK_SIZE_M: tl.constexpr,
    BLOCK_SIZE_N: tl.constexpr,
    NUM_COMM_SMS: tl.constexpr,
    HAS_KV: tl.constexpr = 1,
    NEED_BARRIER: tl.constexpr = 1,
):
    # Compute the starting and ending indices for the current SP rank
    start_idx = cum_seqlen_cpu_tuple[sp_rank]
    end_idx = cum_seqlen_cpu_tuple[sp_rank + 1]
    seq_len = end_idx - start_idx

    # Compute the starting and ending indices for the current SP rank on the GPU
    gpu_start_idx = cum_seqlen_gpu_ptr[sp_rank]
    gpu_end_idx = cum_seqlen_gpu_ptr[sp_rank + 1]

    # Compute the number of blocks and threads per block
    num_blocks = (seq_len + BLOCK_SIZE_M - 1) // BLOCK_SIZE_M
    num_threads = BLOCK_SIZE_M

    # Launch the kernel
    kernel[num_blocks, num_threads](
        gemm_out_ptr,
        gemm_barrier_ptr,
        q_out_ptr,
        k_out_ptr,
        v_out_ptr,
        start_idx,
        end_idx,
        gpu_start_idx,
        gpu_end_idx,
        qkv_out_features,
        head_dim,
        gqa,
        HAS_KV,
        NEED_BARRIER,
    )