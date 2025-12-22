def register_empty_buffer(module, name, buffer, persistent=True):
    """
    Registers an empty buffer with the given module and name.

    Args:
        module (nn.Module): The module to which the buffer should be registered.
        name (str): The name of the buffer.
        buffer (torch.Tensor): The buffer to be registered.
        persistent (bool, optional): Whether the buffer should be considered a persistent state of the module. Defaults to True.
    """
    if persistent:
        module.register_buffer(name, buffer)
    else:
        module.register_parameter(name, buffer)