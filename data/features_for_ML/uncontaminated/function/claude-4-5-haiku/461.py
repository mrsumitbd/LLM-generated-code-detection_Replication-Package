def register_empty_buffer(module, name, buffer, persistent=True):
    """
    Register an empty buffer to a module.
    
    Args:
        module: The module to register the buffer to
        name: The name of the buffer
        buffer: The buffer tensor to register
        persistent: Whether the buffer should be persistent (saved in state_dict)
    """
    module.register_buffer(name, buffer, persistent=persistent)