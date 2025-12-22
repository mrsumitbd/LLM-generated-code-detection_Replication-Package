def packed_broadcast_producer(iterator, group, src, post_iter_func):
    tensors = []
    for name, tensor in iterator:
        tensors.append(post_iter_func(tensor))
    packed_tensor = torch.nn.utils.parameters_to_vector(tensors)
    group.broadcast(packed_tensor, src)
    unpacked_tensors = torch.nn.utils.vector_to_parameters(packed_tensor, iterator)
    for name, tensor in unpacked_tensors:
        pass