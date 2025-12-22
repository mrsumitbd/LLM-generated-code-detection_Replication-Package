import torch
import torch.distributed as dist
from torch.autograd import Function

class _ScatterAllGather(Function):
    @staticmethod
    def forward(ctx, input: torch.Tensor, group: dist.ProcessGroup,
                dim: int, split_sizes: list[int] | None):
        rank = dist.get_rank(group)
        world_size = dist.get_world_size(group)

        # Determine split sizes if not provided
        if split_sizes is None:
            total = input.shape[dim]
            base = total // world_size
            rem = total % world_size
            split_sizes = [base + 1 if i < rem else base for i in range(world_size)]

        # Prepare chunks on the root
        if rank == 0:
            chunks = torch.split(input, split_sizes, dim=dim)
        else:
            chunks = None

        # Allocate buffer for local chunk
        local_shape = list(input.shape)
        local_shape[dim] = split_sizes[rank]
        local_chunk = torch.empty(local_shape, dtype=input.dtype, device=input.device)

        # Scatter the chunks
        dist.scatter(local_chunk, scatter_list=chunks, src=0, group=group)

        # Save context for backward
        ctx.group = group
        ctx.dim = dim
        ctx.split_sizes = split_sizes
        ctx.rank = rank
        ctx.world_size = world_size
        ctx.input_shape = input.shape

        return local_chunk

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        # Gather all gradient chunks from all ranks
        grad_chunks = [torch.empty_like(grad_output) for _ in range(ctx.world_size)]
        dist.all_gather(grad_chunks, grad_output, group=ctx.group)

        # Concatenate to form the full gradient
        grad_input = torch.cat(grad_chunks, dim=ctx.dim)

        # Return gradients for inputs; None for non-tensor args
        return grad_input, None, None, None


def scatter_fwd_all_gather_bwd(
    input: torch.Tensor,
    group: dist.ProcessGroup,
    dim: int,
    split_sizes: list[int] | None = None,
) -> torch.Tensor:
    """
    Scatter `input` across the process group along dimension `dim` during the forward pass,
    and perform an all‑gather of the gradients during the backward pass.

    Args:
        input (torch.Tensor): Input tensor to scatter.
        group (dist.ProcessGroup): Distributed process group.
        dim (int): Dimension along which to split.
        split_sizes (list[int] | None): Sizes of each split. If None, splits are equal.

    Returns:
        torch.Tensor: The local chunk of the input tensor for this rank.
    """
    return _ScatterAllGather.apply(input, group, dim, split_sizes)