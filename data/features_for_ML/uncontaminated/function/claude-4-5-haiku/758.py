def scatter_fwd_all_gather_bwd(
    input: torch.Tensor,
    group: dist.ProcessGroup,
    dim: int,
    split_sizes: list[int] | None = None,
) -> torch.Tensor:
    """
    Scatter in forward pass, all-gather in backward pass.
    """
    return ScatterFwdAllGatherBwd.apply(input, group, dim, split_sizes)


class ScatterFwdAllGatherBwd(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input, group, dim, split_sizes):
        ctx.group = group
        ctx.dim = dim
        ctx.split_sizes = split_sizes
        
        rank = dist.get_rank(group)
        world_size = dist.get_world_size(group)
        
        if split_sizes is None:
            # Evenly split along dim
            size_along_dim = input.size(dim)
            base_size = size_along_dim // world_size
            remainder = size_along_dim % world_size
            split_sizes = [base_size + (1 if i < remainder else 0) for i in range(world_size)]
        
        ctx.split_sizes = split_sizes
        
        # Scatter: each rank gets its portion
        scatter_list = list(torch.split(input, split_sizes, dim=dim))
        output = scatter_list[rank].clone()
        
        return output
    
    @staticmethod
    def backward(ctx, grad_output):
        group = ctx.group
        dim = ctx.dim
        split_sizes = ctx.split_sizes
        
        rank = dist.get_rank(group)
        world_size = dist.get_world_size(group)
        
        # All-gather: collect gradients from all ranks
        grad_list = [torch.zeros_like(grad_output) if i != rank else grad_output 
                     for i in range(world_size)]
        
        dist.all_gather(grad_list, grad_output, group=group)
        
        # Concatenate along dim to get full gradient
        grad_input = torch.cat(grad_list, dim=dim)
        
        return grad_input, None, None, None