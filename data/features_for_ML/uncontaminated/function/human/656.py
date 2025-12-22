import torch
from triton_dist.kernels.nvidia.common_ops import (barrier_on_this_grid, BarrierAllContext)
from triton_dist.utils import (CUDA_CHECK, NVSHMEM_SIGNAL_DTYPE, has_fullmesh_nvlink, has_tma,
                               launch_cooperative_grid_options, nvshmem_barrier_all_on_stream, nvshmem_create_tensors,
                               nvshmem_free_tensor_sync)

def create_reduce_scater_2d_ctx(max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm=True,
                                num_reduction_sms=15) -> ReduceScatter2DContext:
    """
        for num_reduction_sms: tunable param, 16 are enough for H800
            For H800, we overlap local reduce and inter-node p2p with intra-node scatter.
            The reduction kernel bandwidth is not a bottleneck if it exceeds 450GB, so only a few SMs are needed.
            For machines with higher intra_node bandwidth(e.g. H100), we may need to increase the number of SMs or redesign overlapping.
    """
    assert world_size % local_world_size == 0
    assert max_M % world_size == 0

    scatter_bufs = nvshmem_create_tensors((max_M, N), dtype, rank, local_world_size)
    rs_per_node_bufs = nvshmem_create_tensors((max_M // local_world_size, N), dtype, rank, local_world_size)
    p2p_bufs = nvshmem_create_tensors((max_M // local_world_size, N), dtype, rank, local_world_size)

    # signal_buf: scatter_signal | rs_per_node_signal
    num_signal_bufs = 2
    signal_bufs = nvshmem_create_tensors((world_size * num_signal_bufs, ), NVSHMEM_SIGNAL_DTYPE, rank, local_world_size)

    nvshmem_barrier_all_on_stream(torch.cuda.current_stream())

    reduction_stream: torch.cuda.Stream = torch.cuda.Stream(priority=-1)

    num_sync_sms = 0
    num_p2p_sms = 1
    ctx = ReduceScatter2DContext(max_M=max_M, N=N, rank=rank, world_size=world_size, local_world_size=local_world_size,
                                 dtype=dtype, overlap_with_gemm=overlap_with_gemm, scatter_bufs=scatter_bufs,
                                 rs_per_node_bufs=rs_per_node_bufs, p2p_bufs=p2p_bufs, signal_bufs=signal_bufs,
                                 barrier=BarrierAllContext(True), reduction_stream=reduction_stream,
                                 num_sync_sms=num_sync_sms, num_p2p_sms=num_p2p_sms,
                                 num_reduction_sms=num_reduction_sms)
    return ctx