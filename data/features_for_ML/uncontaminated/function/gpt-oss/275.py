import torch

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
    # Collect flattened tensors and their shapes for potential debugging
    flat_tensors = []
    for name, tensor in iterator:
        # Apply post-processing function
        processed = post_iter_func(tensor)
        # Ensure tensor is contiguous and on the same device
        processed = processed.contiguous()
        # Flatten to 1D
        flat_tensors.append(processed.view(-1))

    if not flat_tensors:
        # Nothing to broadcast
        return

    # Concatenate all flattened tensors into a single buffer
    packed = torch.cat(flat_tensors, dim=0)

    # Broadcast the packed buffer from the source rank to all ranks
    # The group is expected to have a broadcast method similar to torch.distributed
    group.broadcast(packed, src=src)

    # No return value needed; the broadcasted buffer is now available on all ranks