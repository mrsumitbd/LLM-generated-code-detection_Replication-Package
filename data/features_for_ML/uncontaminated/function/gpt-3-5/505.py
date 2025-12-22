def kernel_inter_node_p2p_for_same_local_rank(offset, local_world_size, M_per_rank, N, input, output):
    for i in range(M_per_rank):
        for j in range(N):
            output[i][j] = input[(offset + i) % local_world_size * M_per_rank + i][j]