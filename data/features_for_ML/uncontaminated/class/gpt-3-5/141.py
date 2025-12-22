class RedisLimitAtomicActionCoreMixin:
    """Core mixin for RedisLimitAtomicAction."""

    def __init__(self, backend: "RedisStoreBackend"):
        self.backend = backend

class RedisStoreBackend:
    pass

# Example usage
backend = RedisStoreBackend()
core_mixin = RedisLimitAtomicActionCoreMixin(backend)