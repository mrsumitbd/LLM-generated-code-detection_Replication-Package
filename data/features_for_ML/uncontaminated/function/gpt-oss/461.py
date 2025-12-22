import torch

def register_empty_buffer(module, name, buffer, persistent=True):
    """
    Register a buffer to a PyTorch module. If the buffer is None, an empty tensor
    is created. The buffer is set to not require gradients and is registered
    with the given persistence flag.
    """
    # Ensure we have a tensor
    if buffer is None:
        buffer = torch.empty(0)
    elif not isinstance(buffer, torch.Tensor):
        buffer = torch.tensor(buffer)

    # Buffers should not require gradients
    buffer.requires_grad_(False)

    # Register the buffer with the module
    module.register_buffer(name, buffer, persistent=persistent)