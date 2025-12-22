def kernel_all2all_pull_intra_node_nvl(
    gemm_out_ptr,
    gemm_barrier_ptr,
    cum_seqlen_cpu_tuple,  # sp_size + 1 elems
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
    pid = tl.program_id(0)
    
    if NEED_BARRIER:
        tl.cuda.experimental.sm_barrier_init(gemm_barrier_ptr, NUM_COMM_SMS)
    
    # Wait for GEMM to complete
    if NEED_BARRIER:
        tl.cuda.experimental.sm_barrier_wait(gemm_barrier_ptr)
    
    # Load cumulative sequence lengths
    cum_seqlen = tl.zeros((sp_size + 1,), dtype=tl.int32)
    for i in range(sp_size + 1):
        cum_seqlen[i] = cum_seqlen_cpu_tuple[i]
    
    # Calculate sequence lengths per rank
    seqlen_per_rank = tl.zeros((sp_size,), dtype=tl.int32)
    for i in range(sp_size):
        seqlen_per_rank[i] = cum_seqlen[i + 1] - cum_seqlen[i]
    
    # Get local sequence length
    local_seqlen = seqlen_per_rank[sp_rank]
    
    # Calculate offsets for Q, K, V
    q_offset = cum_seqlen[sp_rank] * qkv_out_features
    
    # Process Q output
    num_q_blocks = tl.cdiv(local_seqlen, BLOCK_SIZE_M)
    num_features_blocks = tl.cdiv(qkv_out_features, BLOCK_SIZE_N)
    
    for block_m in range(num_q_blocks):
        for block_n in range(num_features_blocks):
            m_start = block_m * BLOCK_SIZE_M
            n_start = block_n * BLOCK_SIZE_N
            
            m_end = tl.minimum(m_start + BLOCK_SIZE_M, local_seqlen)
            n_end = tl.minimum(n_start + BLOCK_SIZE_N, qkv_out_features)
            
            for m in range(m_start, m_end):
                for n in range(n_start, n_end):
                    src_idx = m * qkv_out_features + n
                    dst_idx = (cum_seqlen[sp_rank] + m) * qkv_out_features + n
                    
                    val = tl.load(gemm_out_ptr + src_idx)
                    tl.store(q_out_ptr + dst_idx, val)
    
    # Process K, V outputs if present
    if HAS_KV:
        kv_features = qkv_out_features // gqa
        kv_offset = cum_seqlen[sp_rank] * kv_features
        
        num_kv_blocks = tl.cdiv(local_seqlen, BLOCK_SIZE_M)
        num_kv_features_blocks = tl.cdiv(kv_features, BLOCK_SIZE_N)
        
        # Process K
        for block_m in range(num_kv_blocks):
            for block_n in range(num_kv_features_blocks):
                m_start = block_m * BLOCK_SIZE_M
                n_start = block_n * BLOCK_SIZE_N
                
                m_end = tl.minimum(m_start + BLOCK_SIZE_M, local_seqlen)
                n_end = tl.minimum(n_start + BLOCK_SIZE_N, kv_features)
                
                for m in range(m_start, m_end):
                    for n in range(n_start, n_end):
                        src_idx = local_seqlen * qkv_out_features + m * kv_features + n
                        dst_idx = (cum_seqlen[sp_rank] + m) * kv_features + n
                        
                        val = tl.load(gemm_out_ptr + src_idx)
                        tl.store(k_out_ptr + dst_idx, val)
        
        # Process V
        for block_m in range(num_kv_blocks):
            for block_n in range(num_kv_features_blocks):
                m_start = block_m * BLOCK_SIZE_M
                n_start = block_n * BLOCK_SIZE_N
                
                m_end = tl.minimum(m_start + BLOCK_SIZE_M, local_seqlen)
                n_end = tl.minimum(n_start + BLOCK_SIZE_N, kv_features)
                
                for m in range(m_start, m_end):
                    for n in range(n_start, n_end):
                        src_idx = local_seqlen * qkv_out_features + local_seqlen * kv_features + m * kv_features + n
                        dst_idx = (cum_seqlen[sp_rank] + m) * kv_features + n
                        
                        val = tl.load(gemm_out_ptr + src_idx)
                        tl.store(v_out_ptr + dst_idx, val)