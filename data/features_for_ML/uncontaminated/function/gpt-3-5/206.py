def ring_reduce_after_scatter(rank, num_ranks, scatter_out, stream):
    import cupy as cp

    M, N = scatter_out.shape
    recv_buf = cp.zeros((M, N), dtype=cp.float32)
    stream.synchronize()

    for i in range(num_ranks - 1):
        send_idx = (rank - i) % num_ranks
        recv_idx = (rank - i - 1) % num_ranks

        send_req = cp.cuda.Stream.null.ptr
        recv_req = cp.cuda.Stream.null.ptr

        if send_idx == rank:
            send_req = stream.record()
            cp.cuda.Stream.null.synchronize()

        if recv_idx == rank:
            recv_req = stream.record()
            cp.cuda.Stream.null.synchronize()

        if send_req:
            cp.cuda.nvtx.RangePush(f"send_{send_idx}")
            cp.cuda.nvtx.RangePop()

        if recv_req:
            cp.cuda.nvtx.RangePush(f"recv_{recv_idx}")
            cp.cuda.nvtx.RangePop()

        stream.synchronize()

    return recv_buf