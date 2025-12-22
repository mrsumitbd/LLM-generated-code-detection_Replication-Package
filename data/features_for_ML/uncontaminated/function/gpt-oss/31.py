# A simple global registry that can be cleared by `unregister`.
_registry = {}

def unregister():
    """
    Clears the global registry.

    This function is intended to be used in contexts where a global
    registry (e.g., of callbacks, handlers, or plugin classes) is
    maintained. Calling `unregister()` will remove all entries from
    the registry, effectively unregistering everything that was
    previously registered.

    The function is safe to call even if the registry is already
    empty.
    """
    global _registry
    _registry.clear()