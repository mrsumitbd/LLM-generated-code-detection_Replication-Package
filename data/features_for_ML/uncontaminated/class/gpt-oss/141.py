from __future__ import annotations

class RedisLimitAtomicActionCoreMixin:
    """Core mixin for RedisLimitAtomicAction."""

    def __init__(self, backend: "RedisStoreBackend"):
        # Store the backend instance for later use
        self.backend = backend

        # Prefix used for lock keys to avoid collisions
        self._lock_key_prefix = "redis_limit_atomic_action_lock:"

    # Helper to construct a lock key for a given resource
    def _lock_key(self, resource: str) -> str:
        return f"{self._lock_key_prefix}{resource}"