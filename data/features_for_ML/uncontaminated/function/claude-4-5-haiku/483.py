def chunk_kkt_inv_ut_fused_kernel(
    k,
    v,
    beta,
    g,
    cu_seqlens,
    chunk_indices,
    A,  # tmp buffer [B, T, H, BT]
    g_cumsum,  # output buffer1 [B, T, H, BT]
    Ai,  # output buffer2 [B, T, H, BT]
    w,  # output buffer3 [B, T, H, K]
    u,  # output buffer4 [B, T, H, V]
    T,
    NT,
    H: tl.constexpr,
    K: tl.constexpr,
    V: tl.constexpr,
    BT: tl.constexpr,  # chunk size
    BK: tl.constexpr,
    BV: tl.constexpr,
    USE_G: tl.constexpr = True,
):
    pid_b = tl.program_id(0)
    pid_h = tl.program_id(1)
    pid_t = tl.program_id(2)
    
    # Get sequence boundaries
    cu_seqlens_b = tl.load(cu_seqlens + pid_b)
    cu_seqlens_b1 = tl.load(cu_seqlens + pid_b + 1)
    seq_len = cu_seqlens_b1 - cu_seqlens_b
    
    # Get chunk boundaries
    chunk_start = tl.load(chunk_indices + pid_t)
    chunk_end = tl.load(chunk_indices + pid_t + 1)
    chunk_len = tl.minimum(chunk_end - chunk_start, BT)
    
    # Offsets for this chunk
    offset_t = tl.arange(0, BT)
    offset_k = tl.arange(0, BK)
    offset_v = tl.arange(0, BV)
    
    # Initialize accumulators
    g_cumsum_val = tl.zeros((BT,), dtype=tl.float32)
    A_val = tl.zeros((BT, BT), dtype=tl.float32)
    Ai_val = tl.zeros((BT, BT), dtype=tl.float32)
    w_acc = tl.zeros((BT, BK), dtype=tl.float32)
    u_acc = tl.zeros((BT, BV), dtype=tl.float32)
    
    # Load g values for cumsum if needed
    if USE_G:
        for i in range(BT):
            pos = chunk_start + i
            if pos < seq_len:
                g_idx = cu_seqlens_b + pos
                g_val = tl.load(g + g_idx * H + pid_h)
                if i == 0:
                    g_cumsum_val[i] = g_val
                else:
                    g_cumsum_val[i] = g_cumsum_val[i-1] + g_val
    
    # Compute A matrix (attention scores within chunk)
    for i in range(BT):
        pos_i = chunk_start + i
        if pos_i >= seq_len:
            break
        
        for j in range(BT):
            pos_j = chunk_start + j
            if pos_j >= seq_len or pos_j > pos_i:
                break
            
            # Load k[pos_j] and v[pos_i]
            k_idx = (cu_seqlens_b + pos_j) * H * K + pid_h * K
            v_idx = (cu_seqlens_b + pos_i) * H * V + pid_h * V
            
            # Compute dot product k @ v
            score = tl.zeros((), dtype=tl.float32)
            for kk in tl.range(0, K, BK):
                k_block = tl.load(k + k_idx + kk + offset_k, mask=kk + offset_k < K, other=0.0)
                v_block = tl.load(v + v_idx + kk + offset_k, mask=kk + offset_k < K, other=0.0)
                score += tl.sum(k_block * v_block)
            
            # Load beta and apply
            beta_idx = (cu_seqlens_b + pos_i) * H + pid_h
            beta_val = tl.load(beta + beta_idx)
            
            A_val[i, j] = score * beta_val
    
    # Compute Ai (inverse of A)
    for i in range(BT):
        for j in range(BT):
            if i == j:
                Ai_val[i, j] = 1.0 / (A_val[i, j] + 1e-6)
            else:
                Ai_val[i, j] = 0.0
    
    # Compute w and u
    for i in range(BT):
        pos_i = chunk_start + i
        if pos_i >= seq_len:
            break
        
        # Compute w[i] = sum_j Ai[i,j] * k[j]
        for kk in tl.range(0, K, BK):
            w_val = tl.zeros((BK,), dtype=tl.float32)
            for j in range(BT):
                pos_j = chunk_start + j
                if pos_j >= seq_len or pos_j > pos_i:
                    break
                k_idx = (cu_seqlens_b + pos_j) * H * K + pid_h * K + kk
                k_block = tl.load(k + k_idx + offset_k, mask=kk + offset_k < K, other=0.0)
                w_val += Ai_val[i, j] * k_block
            w_acc[i, kk:kk+BK] = w_val
        
        # Compute u[i] = sum_j Ai[i,j] * v[j]
        for vv in tl.range(0, V, BV):
            u_val = tl.zeros((BV,), dtype=tl.float32)
            for j in range(BT):
                pos_j = chunk_start + j
                if pos_j >= seq_len or pos_j > pos_i:
                    break
                v_idx = (cu_seqlens_b + pos_j) * H * V + pid_h * V + vv
                v_block = tl.load(v + v_idx + offset_v, mask=vv + offset_v < V, other=0.0)
                u_val += Ai_val[i, j] * v_block
            u_acc[i, vv:vv+BV] = u_val
    
    # Store results
    for i in range(BT):
        pos_i = chunk_start + i
        if pos_i >= seq_len:
            break
        
        # Store g_cumsum
        g_cumsum_idx = pid_b * T * H * BT + pos_i * H * BT + pid_h * BT + i
        tl.store(g_cumsum + g_cumsum_idx, g_cumsum_val[i])
        
        # Store A and Ai
        for j in range(BT):
            A_idx = pid_b * T * H * BT + pos_i * H * BT + pid_h * BT + j
            Ai_idx = pid_b * T * H * BT + pos_i * H * BT + pid_h * BT + j
            tl.store(A + A_idx, A_val[i, j])
            tl.store(Ai + Ai_idx, Ai_val[i, j])
        
        # Store w and u
        for kk in range(K):
            w_idx = pid_b * T * H * K + pos_i * H * K + pid_h * K + kk
            tl.store(w + w_idx, w_acc[i, kk])
        
        for vv in range(V):
            u_idx = pid_b * T * H * V + pos_i * H * V + pid_h * V + vv
            tl.store(u + u_idx, u_acc[i, vv])