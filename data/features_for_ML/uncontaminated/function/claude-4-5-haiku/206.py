def ring_reduce_after_scatter(
    rank,
    num_ranks,
    scatter_out,  # [M, N]
    stream,
):
    """
    Perform ring reduce-scatter operation after scatter.
    
    In a ring reduce-scatter:
    - Each rank i sends its data to rank (i+1) % num_ranks
    - Each rank i receives data from rank (i-1) % num_ranks
    - Data is accumulated at each step
    - After num_ranks-1 steps, each rank has the reduced result for its chunk
    """
    import torch
    import torch.distributed as dist
    
    M, N = scatter_out.shape
    chunk_size = N // num_ranks
    
    # Create a copy to work with
    result = scatter_out.clone()
    
    # Ring reduce-scatter: num_ranks - 1 iterations
    for step in range(num_ranks - 1):
        # Determine which chunk this rank sends and receives
        send_rank = (rank - step) % num_ranks
        recv_rank = (rank + 1) % num_ranks
        
        # Prepare send and receive buffers
        send_chunk_idx = send_rank
        recv_chunk_idx = (send_rank + 1) % num_ranks
        
        send_buf = result[:, send_chunk_idx * chunk_size:(send_chunk_idx + 1) * chunk_size].contiguous()
        recv_buf = torch.zeros_like(send_buf)
        
        # Send to next rank, receive from previous rank
        send_req = dist.isend(send_buf, dst=recv_rank)
        recv_req = dist.irecv(recv_buf, src=(rank - 1) % num_ranks)
        
        send_req.wait()
        recv_req.wait()
        
        # Accumulate received data into the appropriate chunk
        result[:, recv_chunk_idx * chunk_size:(recv_chunk_idx + 1) * chunk_size] += recv_buf
    
    # After ring reduce-scatter, each rank has its reduced chunk
    # Extract the final result for this rank
    final_chunk_idx = rank
    final_result = result[:, final_chunk_idx * chunk_size:(final_chunk_idx + 1) * chunk_size].clone()
    
    return final_result