def call_ag():
        cp_engine_producer_all_gather_full_mesh_push_multi_stream(rank, num_ranks, a, workspace_tensors, one,
                                                                  M_PER_CHUNK, ag_streams, barrier_tensors)