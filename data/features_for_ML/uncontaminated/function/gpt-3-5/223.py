def create_fast_allgather_context(rank, node, num_ranks, num_nodes, max_buffer_size: int = 2 * 32 * 1024 * 1024):
    context = {
        'rank': rank,
        'node': node,
        'num_ranks': num_ranks,
        'num_nodes': num_nodes,
        'max_buffer_size': max_buffer_size
    }
    return context