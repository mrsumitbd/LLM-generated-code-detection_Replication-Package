def native_group_cast_impl(
    input: torch.Tensor,
    output: torch.Tensor | None,
    input_split_sizes: list[int] | torch.Tensor,
    output_split_sizes: list[int] | torch.Tensor,
    dst_indices: list[list[int]] | torch.Tensor,
    src_index: list[int] | torch.Tensor,
    group: dist.ProcessGroup,
    async_op: bool = False,
    cast_lse: bool = False,
    input_lse: torch.Tensor | None = None,
    output_lse: torch.Tensor | None = None,
    **kwargs,
) -> WorkWithPostProcessFn:
    """Native group-cast implementation"""
    
    # Convert to lists if tensors
    if isinstance(input_split_sizes, torch.Tensor):
        input_split_sizes = input_split_sizes.tolist()
    if isinstance(output_split_sizes, torch.Tensor):
        output_split_sizes = output_split_sizes.tolist()
    if isinstance(src_index, torch.Tensor):
        src_index = src_index.tolist()
    if isinstance(dst_indices, torch.Tensor):
        dst_indices = dst_indices.tolist()
    
    # Get rank and world size
    rank = dist.get_rank(group)
    world_size = dist.get_world_size(group)
    
    # Initialize output if not provided
    if output is None:
        output = torch.zeros_like(input)
    
    # Prepare send and receive buffers
    send_buffers = []
    recv_buffers = []
    
    # Split input according to input_split_sizes
    input_splits = torch.split(input, input_split_sizes)
    
    # Prepare output splits
    output_splits = [torch.zeros(size, *input.shape[1:], dtype=input.dtype, device=input.device) 
                     for size in output_split_sizes]
    
    # Create send requests
    send_reqs = []
    for dst_rank_list in dst_indices:
        if rank in dst_rank_list:
            idx = dst_rank_list.index(rank)
            if idx < len(input_splits):
                send_buf = input_splits[idx]
                for dst_rank in dst_rank_list:
                    if dst_rank != rank:
                        req = dist.isend(send_buf, dst=dst_rank, group=group)
                        send_reqs.append(req)
    
    # Create receive requests
    recv_reqs = []
    for src_rank in src_index:
        if src_rank != rank:
            recv_buf = torch.zeros_like(output_splits[src_rank] if src_rank < len(output_splits) else output)
            req = dist.irecv(recv_buf, src=src_rank, group=group)
            recv_reqs.append((req, recv_buf, src_rank))
    
    # Handle LSE if needed
    lse_send_reqs = []
    lse_recv_reqs = []
    if cast_lse and input_lse is not None and output_lse is not None:
        input_lse_splits = torch.split(input_lse, input_split_sizes)
        output_lse_splits = [torch.zeros(size, *input_lse.shape[1:], dtype=input_lse.dtype, device=input_lse.device)
                             for size in output_split_sizes]
        
        for dst_rank_list in dst_indices:
            if rank in dst_rank_list:
                idx = dst_rank_list.index(rank)
                if idx < len(input_lse_splits):
                    for dst_rank in dst_rank_list:
                        if dst_rank != rank:
                            req = dist.isend(input_lse_splits[idx], dst=dst_rank, group=group)
                            lse_send_reqs.append(req)
        
        for src_rank in src_index:
            if src_rank != rank:
                lse_recv_buf = torch.zeros_like(output_lse_splits[src_rank] if src_rank < len(output_lse_splits) else output_lse)
                req = dist.irecv(lse_recv_buf, src=src_rank, group=group)
                lse_recv_reqs.append((req, lse_recv_buf, src_rank))
    
    def post_process_fn():
        # Wait for all sends and receives
        for req in send_reqs:
            req.wait()
        
        for req, recv_buf, src_rank in recv_reqs:
            req.wait()
            if src_rank < len(output_splits):
                output_splits[src_rank] = recv_buf
        
        if cast_lse:
            for req in lse_send_reqs:
                req.wait()
            for req, lse_recv_buf, src_rank in lse_recv_reqs:
                req.wait()
        
        # Concatenate output splits
        if output_splits:
            result = torch.cat(output_splits, dim=0)
            output.copy_(result)
        
        return output
    
    # Create work object
    work = WorkWithPostProcessFn(
        post_process_fn=post_process_fn,
        async_op=async_op
    )
    
    if not async_op:
        post_process_fn()
    
    return work