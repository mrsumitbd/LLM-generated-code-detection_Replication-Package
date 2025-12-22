def kernel_inter_node_p2p_for_same_local_rank(offset, local_world_size, M_per_rank, N, input,  # [M, N]
                                              output,  # [M, N]
                                              ):
    for m in range(M_per_rank):
        for n in range(N):
            output[m, n] = input[m + offset, n]