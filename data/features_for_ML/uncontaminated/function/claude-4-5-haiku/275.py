def packed_broadcast_producer(iterator, group, src, post_iter_func):
    """Broadcast a list of tensors in a packed manner.

    Args:
        iterator: iterator of model parameters. Returns a tuple of (name, tensor)
        group: process group (vllm PyNcclCommunicator)
        src: source rank (0 in current implementation)
        post_iter_func: function to apply to each tensor before packing, should return a tensor

    Returns:
        None

    """
    import torch
    
    # Collect all tensors to broadcast
    tensors_to_pack = []
    tensor_shapes = []
    tensor_dtypes = []
    
    # Iterate through all parameters and apply post_iter_func
    for name, tensor in iterator:
        processed_tensor = post_iter_func(tensor)
        tensors_to_pack.append(processed_tensor)
        tensor_shapes.append(processed_tensor.shape)
        tensor_dtypes.append(processed_tensor.dtype)
    
    if not tensors_to_pack:
        return
    
    # Flatten all tensors into a single buffer
    flattened_tensors = []
    for tensor in tensors_to_pack:
        flattened_tensors.append(tensor.flatten())
    
    packed_tensor = torch.cat(flattened_tensors)
    
    # Broadcast the packed tensor
    group.broadcast(packed_tensor, src=src)