def _get_backend() -> MemoryBackend:
    global _memory
    if _memory is None:
        _memory = _build_backend()  # Works with no arguments
    return _memory