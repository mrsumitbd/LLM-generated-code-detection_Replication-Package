from .backends import BaseStateBackend, _get_backend

def _get_default_backend() -> BaseStateBackend:
    """Get or create the default backend instance.

    Returns:
        The default backend instance.
    """
    global _backend, _middleware_backend

    # First try to use the middleware backend if available
    if _middleware_backend is not None:
        return _middleware_backend

    # Fall back to configured backend or create default env backend
    if _backend is None:
        # Default to environment variable backend
        _backend = _get_backend("env")
    return _backend