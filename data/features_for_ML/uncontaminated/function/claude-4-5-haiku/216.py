def add_continuous(
    lhs: torch.Tensor,
    rhs: torch.Tensor,
    out: Optional[torch.Tensor],
    num_ctas=16,
    num_warps=32,
):
    import triton
    import triton.language as tl
    
    @triton.jit
    def add_kernel(
        lhs_ptr,
        rhs_ptr,
        out_ptr,
        n_elements,
        BLOCK_SIZE: tl.constexpr,
    ):
        pid = tl.program_id(axis=0)
        block_start = pid * BLOCK_SIZE
        offsets = block_start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < n_elements
        
        lhs_vals = tl.load(lhs_ptr + offsets, mask=mask)
        rhs_vals = tl.load(rhs_ptr + offsets, mask=mask)
        result = lhs_vals + rhs_vals
        
        tl.store(out_ptr + offsets, result, mask=mask)
    
    if out is None:
        out = torch.empty_like(lhs)
    
    n_elements = lhs.numel()
    BLOCK_SIZE = 1024
    grid = (triton.cdiv(n_elements, BLOCK_SIZE),)
    
    add_kernel[grid](
        lhs,
        rhs,
        out,
        n_elements,
        BLOCK_SIZE=BLOCK_SIZE,
        num_ctas=num_ctas,
        num_warps=num_warps,
    )
    
    return out