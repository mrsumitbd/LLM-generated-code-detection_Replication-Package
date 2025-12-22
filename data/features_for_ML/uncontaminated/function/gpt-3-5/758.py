import torch
import torch.distributed as dist

def scatter_fwd_all_gather_bwd(input: torch.Tensor, group: dist.ProcessGroup, dim: int, split_sizes: list[int] | None = None) -> torch.Tensor:
    if split_sizes is None:
        split_sizes = [input.size(dim) // dist.get_world_size()] * dist.get_world_size()
    else:
        assert sum(split_sizes) == input.size(dim), "Sum of split sizes must equal the input size along the specified dimension"

    scattered_tensors = input.split(split_sizes, dim=dim)
    dist.scatter(scattered_tensors, scatter_gather_list=None, src=0, group=group)
    gathered_tensors = [torch.empty_like(tensor) for tensor in scattered_tensors]
    dist.all_gather(gathered_tensors, scattered_tensors, group=group)

    return torch.cat(gathered_tensors, dim=dim)