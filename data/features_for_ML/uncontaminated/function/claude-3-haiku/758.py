import torch
import torch.distributed as dist

def scatter_fwd_all_gather_bwd(
    input: torch.Tensor,
    group: dist.ProcessGroup,
    dim: int,
    split_sizes: list[int] | None = None,
) -> torch.Tensor:
    world_size = dist.get_world_size(group)
    rank = dist.get_rank(group)

    if split_sizes is None:
        split_sizes = [input.size(dim) // world_size] * world_size

    scattered_input = torch.zeros_like(input)
    dist.scatter(scattered_input, [input] if rank == 0 else [], split_sizes, dim, group)

    all_gathered_input = torch.zeros_like(input)
    dist.all_gather(all_gathered_input, scattered_input, group)

    return all_gathered_input