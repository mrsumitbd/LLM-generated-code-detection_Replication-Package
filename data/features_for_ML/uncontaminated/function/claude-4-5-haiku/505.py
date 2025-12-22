def kernel_inter_node_p2p_for_same_local_rank(offset, local_world_size, M_per_rank, N, input,  # [M, N]
                                              output,  # [M, N]
                                              ):
    """
    Kernel for inter-node point-to-point communication for ranks with the same local rank.
    
    This function performs a gather operation where each rank sends its portion of data
    to a specific location in the output buffer based on the offset and local_world_size.
    
    Args:
        offset: Starting offset in the output buffer
        local_world_size: Number of ranks per node
        M_per_rank: Number of rows per rank
        N: Number of columns
        input: Input tensor of shape [M, N] where M = M_per_rank * local_world_size
        output: Output tensor of shape [M, N]
    """
    M = M_per_rank * local_world_size
    
    # Each rank processes its portion of data
    # The data from input is placed into output at positions determined by offset and local_world_size
    for i in range(M_per_rank):
        for j in range(N):
            # Calculate source index in input
            src_idx = i * N + j
            
            # Calculate destination index in output
            # Data is interleaved based on local_world_size
            dst_row = offset + i * local_world_size
            dst_idx = dst_row * N + j
            
            output[dst_idx] = input[src_idx]