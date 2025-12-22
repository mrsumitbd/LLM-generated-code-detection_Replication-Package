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
    tensors = []
    names = []
    for name, tensor in iterator:
        tensors.append(post_iter_func(tensor))
        names.append(name)

    group.broadcast_packed(tensors, src)