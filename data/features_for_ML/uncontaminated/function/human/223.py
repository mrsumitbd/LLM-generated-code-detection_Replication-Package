import torch
from triton_dist.utils import NVSHMEM_SIGNAL_DTYPE, nvshmem_free_tensor_sync, nvshmem_create_tensor

def create_fast_allgather_context(rank, node, num_ranks, num_nodes, max_buffer_size: int = 2 * 32 * 1024 * 1024):
    signal_tensor = nvshmem_create_tensor((num_ranks, ), NVSHMEM_SIGNAL_DTYPE)
    signal_tensor.zero_()
    ll_buffers = [nvshmem_create_tensor((max_buffer_size, ), torch.int8) for _ in range(2)]
    grid_barrier = torch.zeros((1, ), dtype=torch.uint32, device="cuda")

    ctx = FastAllGatherContext(
        rank=rank,
        node=node,
        num_ranks=num_ranks,
        num_nodes=num_nodes,
        signal_tensor=signal_tensor,
        ll_buffers=ll_buffers,
        grid_barrier=grid_barrier,
        max_buffer_size=max_buffer_size,
        signal_target=15,
    )

    return ctx