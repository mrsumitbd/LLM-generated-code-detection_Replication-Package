class RedisLimitAtomicActionCoreMixin:
    """Core mixin for RedisLimitAtomicAction."""

    def __init__(self, backend: "RedisStoreBackend"):
        self.backend = backend