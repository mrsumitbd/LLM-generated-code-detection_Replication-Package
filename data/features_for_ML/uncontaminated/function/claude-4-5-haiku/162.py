def _get_backend() -> MemoryBackend:
    global _backend
    if _backend is None:
        _backend = MemoryBackend()
    return _backend