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
    target_packed_tensor_size = get_target_packed_tensor_size()

    num_buffers = get_num_buffers()
    streams = [torch.cuda.Stream() for _ in range(num_buffers)]
    buffer_idx = 0

    packing_tensor_list = [[] for _ in range(num_buffers)]
    packing_tensor_sizes = [0 for _ in range(num_buffers)]
    packed_tensors = [
        torch.empty(0, dtype=torch.uint8, device="cuda") for _ in range(num_buffers)
    ]

    while True:
        # Move to the next buffer
        buffer_idx = (buffer_idx + 1) % num_buffers
        # Synchronize the current stream
        streams[buffer_idx].synchronize()
        # Start tasks for the new buffer in a new stream
        with torch.cuda.stream(streams[buffer_idx]):  # type: ignore[arg-type]
            try:
                # Initialize the packing tensor list and sizes
                packing_tensor_list[buffer_idx] = []
                packing_tensor_sizes[buffer_idx] = 0
                # Pack the tensors
                while True:
                    # Apply backend specific post processing and then convert to linearized uint8 tensor
                    tensor = post_iter_func(next(iterator)).view(torch.uint8).view(-1)
                    packing_tensor_list[buffer_idx].append(tensor)
                    packing_tensor_sizes[buffer_idx] += tensor.view(torch.uint8).numel()
                    if packing_tensor_sizes[buffer_idx] > target_packed_tensor_size:
                        break
                # Pack the tensors and call broadcast collective
                packed_tensors[buffer_idx] = torch.cat(
                    packing_tensor_list[buffer_idx], dim=0
                )
                group.broadcast(packed_tensors[buffer_idx], src=src)
            except StopIteration:
                # do the last broadcast if there are remaining tensors
                if len(packing_tensor_list[buffer_idx]) > 0:
                    packed_tensors[buffer_idx] = torch.cat(
                        packing_tensor_list[buffer_idx], dim=0
                    )
                    group.broadcast(packed_tensors[buffer_idx], src=src)
                break