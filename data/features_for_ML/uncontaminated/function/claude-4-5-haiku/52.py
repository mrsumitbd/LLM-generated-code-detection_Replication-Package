def gemm_act_tuned(
    A: Tensor,
    B: Tensor,
    preact_out: Optional[Tensor],
    postact_out: Tensor,
    C: Optional[Tensor] = None,
    bias: Optional[Tensor] = None,
    activation: Literal[None, "relu", "relu_sq", "gelu_tanh_approx"] = None,
    cu_seqlens_m: Optional[Tensor] = None,
    A_idx: Optional[Tensor] = None,
    dynamic_scheduler: bool = False,
    config: Optional[GemmConfig] = None,
) -> None:
    import torch
    import triton
    import triton.language as tl
    
    if config is None:
        config = GemmConfig()
    
    # Determine if we're using variable length sequences
    varlen_m = cu_seqlens_m is not None
    gather_A = A_idx is not None
    
    # Get dimensions
    if varlen_m:
        total_M = A.shape[0]
        K = A.shape[1]
        L = cu_seqlens_m.shape[0] - 1
    else:
        M = A.shape[0]
        K = A.shape[1]
        L = 1
    
    if B.dim() == 2:
        K_b, N = B.shape
    else:
        L_b, K_b, N = B.shape
    
    assert K == K_b, f"K mismatch: {K} vs {K_b}"
    
    # Determine grid
    if varlen_m:
        total_M_val = total_M
    else:
        total_M_val = M
    
    grid = lambda META: (
        triton.cdiv(total_M_val, META['BLOCK_M']) * triton.cdiv(N, META['BLOCK_N']),
        L if L > 1 else 1,
    )
    
    @triton.jit
    def kernel_gemm_act(
        A_ptr, B_ptr, C_ptr, bias_ptr, preact_ptr, postact_ptr,
        cu_seqlens_m_ptr, A_idx_ptr,
        M, N, K, L,
        stride_am, stride_ak,
        stride_bk, stride_bn,
        stride_cm, stride_cn,
        stride_bias,
        BLOCK_M: tl.constexpr,
        BLOCK_N: tl.constexpr,
        BLOCK_K: tl.constexpr,
        activation_type: tl.constexpr,
        has_bias: tl.constexpr,
        has_C: tl.constexpr,
        has_preact: tl.constexpr,
        varlen_m: tl.constexpr,
        gather_A: tl.constexpr,
    ):
        pid_m = tl.program_id(0)
        pid_n = tl.program_id(1)
        pid_l = tl.program_id(2) if L > 1 else 0
        
        m_offset = pid_m * BLOCK_M
        n_offset = pid_n * BLOCK_N
        
        if varlen_m:
            seq_start = tl.load(cu_seqlens_m_ptr + pid_l)
            seq_end = tl.load(cu_seqlens_m_ptr + pid_l + 1)
            seq_len = seq_end - seq_start
            m_offset = seq_start + pid_m * BLOCK_M
        
        m_idx = tl.arange(0, BLOCK_M)
        n_idx = tl.arange(0, BLOCK_N)
        k_idx = tl.arange(0, BLOCK_K)
        
        acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)
        
        for k in range(0, K, BLOCK_K):
            k_remaining = tl.minimum(BLOCK_K, K - k)
            
            if gather_A:
                a_idx = tl.load(A_idx_ptr + m_offset + m_idx[:, None])
                A_block = tl.load(
                    A_ptr + a_idx[:, None] * stride_am + (k + k_idx[None, :]) * stride_ak,
                    mask=(m_idx[:, None] < BLOCK_M) & (k_idx[None, :] < k_remaining),
                    other=0.0
                )
            else:
                A_block = tl.load(
                    A_ptr + (m_offset + m_idx[:, None]) * stride_am + (k + k_idx[None, :]) * stride_ak,
                    mask=(m_idx[:, None] < BLOCK_M) & (k_idx[None, :] < k_remaining),
                    other=0.0
                )
            
            if B.dim() == 2:
                B_block = tl.load(
                    B_ptr + (k + k_idx[:, None]) * stride_bk + (n_offset + n_idx[None, :]) * stride_bn,
                    mask=(k_idx[:, None] < k_remaining) & (n_idx[None, :] < BLOCK_N),
                    other=0.0
                )
            else:
                B_block = tl.load(
                    B_ptr + pid_l * B.stride(0) + (k + k_idx[:, None]) * stride_bk + (n_offset + n_idx[None, :]) * stride_bn,
                    mask=(k_idx[:, None] < k_remaining) & (n_idx[None, :] < BLOCK_N),
                    other=0.0
                )
            
            acc += tl.dot(A_block, B_block)
        
        if has_bias:
            if bias.dim() == 1:
                bias_val = tl.load(bias_ptr + n_offset + n_idx[None, :])
            else:
                bias_val = tl.load(bias_ptr + pid_l * stride_bias + n_offset + n_idx[None, :])
            acc += bias_val
        
        if has_C:
            C_block = tl.load(
                C_ptr + (m_offset + m_idx[:, None]) * stride_cm + (n_offset + n_idx[None, :]) * stride_cn,
                mask=(m_idx[:, None] < BLOCK_M) & (n_idx[None, :] < BLOCK_N),
                other=0.0
            )
            acc += C_block
        
        if has_preact:
            tl.store(
                preact_ptr + (m_offset + m_idx[:, None]) * stride_cm + (n_offset + n_idx[None, :]) * stride_cn,
                acc,
                mask=(m_idx[:, None] < BLOCK_M) & (n_idx[None, :] < BLOCK_N)
            )
        
        if activation_type == "relu":
            acc = tl.maximum(acc, 0.0)
        elif activation_type == "relu_sq":
            acc = tl.maximum(acc, 0.0)
            acc = acc * acc
        elif activation_type == "gelu_tanh_approx":
            acc = 0.5 * acc * (1.0 + tl.tanh(0.7978845608 * (acc + 0.044715 * acc * acc * acc)))
        
        tl.store(
            postact_ptr + (m_offset + m_idx[:, None]) * stride_cm + (n_offset + n_idx[None, :]) * stride_cn,
            acc,
            mask=(m_idx[:, None] < BLOCK_M) & (n_idx[None, :] < BLOCK_N)
        )
    
    activation_type = activation if activation else None
    
    kernel_gemm_act[grid](
        A, B, C, bias, preact_out, postact_out,
        cu_seqlens_m, A_idx,
        A.shape[0] if not varlen_m else total_M,
        B.shape[-1], K, L,
        A.stride(0), A.stride(1),
        B.stride(-2), B.stride(-1),
        postact_out.stride(0), postact_out.stride(1),
        bias.stride(0) if bias and bias.dim() > 1 else 0,
        BLOCK_M=config.BLOCK_M,
        BLOCK_N=config.BLOCK_N,
        BLOCK_K=config.BLOCK_K,
        activation_type=activation_type,
        has_bias=bias is not None,
        has_C=C is not None,
        has_preact=preact_out is not None,
        varlen_m=varlen_m,
        gather_A=gather_A,
    )