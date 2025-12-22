def register_empty_buffer(module, name, buffer, persistent=True):
    if persistent:
        module.register_buffer(name, buffer)
    else:
        setattr(module, name, buffer)