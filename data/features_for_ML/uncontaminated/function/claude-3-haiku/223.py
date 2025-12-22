import torch.distributed as dist
import torch

def create_fast_allgather_context(rank, node, num_ranks, num_nodes, max_buffer_size: int = 2 * 32 * 1024 * 1024):
    group = dist.new_group(list(range(num_ranks)))
    world_size = dist.get_world_size(group)
    tensor_size = max_buffer_size // (world_size * 4)  # Assuming 4 bytes per float
    tensor = torch.zeros(tensor_size, dtype=torch.float32)

    def allgather(input_tensor):
        output_tensors = [torch.zeros_like(tensor) for _ in range(world_size)]
        dist.all_gather(output_tensors, input_tensor, group=group)
        return torch.cat(output_tensors, dim=0)

    return allgather