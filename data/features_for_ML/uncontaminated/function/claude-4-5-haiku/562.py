def _get_default_backend() -> BaseStateBackend:
    """Get or create the default backend instance.

    Returns:
        The default backend instance.
    """
    global _default_backend
    
    if _default_backend is None:
        _default_backend = BaseStateBackend()
    
    return _default_backend