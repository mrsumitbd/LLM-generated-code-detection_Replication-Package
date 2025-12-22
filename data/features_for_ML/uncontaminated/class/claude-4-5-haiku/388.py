class InstancePoolManager:
    """Manager for `InstancePool`"""

    def __init__(self, pool: InstancePool):
        self.pool = pool

    def __enter__(self):
        return self.pool

    def __exit__(self, *_):
        self.pool.shutdown()