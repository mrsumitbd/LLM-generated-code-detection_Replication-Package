def create_reduce_scater_2d_ctx(max_M, N, rank, world_size, local_world_size, dtype, overlap_with_gemm=True,
                                num_reduction_sms=15) -> ReduceScatter2DContext:
    """
        for num_reduction_sms: tunable param, 16 are enough for H800
            For H800, we overlap local reduce and inter-node p2p with intra-node scatter.
            The reduction kernel bandwidth is not a bottleneck if it exceeds 450GB, so only a few SMs are needed.
            For machines with higher intra_node bandwidth(e.g. H100), we may need to increase the number of SMs or redesign overlapping.
    """
    import torch
    from torch.distributed import get_rank, get_world_size
    
    # Calculate local rank and inter-node rank
    local_rank = rank % local_world_size
    inter_node_rank = rank // local_world_size
    num_nodes = world_size // local_world_size
    
    # Calculate dimensions for 2D reduce-scatter
    # M is split across nodes, N is split across local ranks
    M_per_node = max_M // num_nodes
    N_per_rank = N // local_world_size
    
    # Get dtype size in bytes
    dtype_size = torch.tensor([], dtype=dtype).element_size()
    
    # Create context object
    ctx = ReduceScatter2DContext(
        max_M=max_M,
        N=N,
        rank=rank,
        world_size=world_size,
        local_world_size=local_world_size,
        local_rank=local_rank,
        inter_node_rank=inter_node_rank,
        num_nodes=num_nodes,
        M_per_node=M_per_node,
        N_per_rank=N_per_rank,
        dtype=dtype,
        dtype_size=dtype_size,
        overlap_with_gemm=overlap_with_gemm,
        num_reduction_sms=num_reduction_sms
    )
    
    return ctx