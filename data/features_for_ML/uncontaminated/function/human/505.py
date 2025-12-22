import triton.language as tl
from triton_dist.language.extra import libshmem_device
import triton_dist.language as dl

def kernel_inter_node_p2p_for_same_local_rank(offset, local_world_size, M_per_rank, N, input,  # [M, N]
                                              output,  # [M, N]
                                              ):
    rank = dl.rank()
    world_size = dl.num_ranks()
    node_id = rank // local_world_size
    nnodes = world_size // local_world_size
    local_rank = rank % local_world_size
    nelem_per_rank = M_per_rank * N

    remote_node_id = (offset + 1 + node_id) % nnodes
    remote_rank = local_rank + remote_node_id * local_world_size
    elem_size = tl.constexpr(input.dtype.element_ty.primitive_bitwidth) // 8
    libshmem_device.putmem_block(
        output + node_id * nelem_per_rank,
        input + remote_node_id * nelem_per_rank,
        nelem_per_rank * elem_size,
        remote_rank,
    )