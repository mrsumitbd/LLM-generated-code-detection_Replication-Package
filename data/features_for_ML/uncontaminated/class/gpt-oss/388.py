class InstancePoolManager:
    """Manager for `InstancePool`"""

    def __init__(self, pool: InstancePool):
        self._pool = pool
        self._instance = None

    def __enter__(self):
        self._instance = self._pool.acquire()
        return self._instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._instance is not None:
            self._pool.release(self._instance)
            self._instance = None
        # Do not suppress exceptions
        return False