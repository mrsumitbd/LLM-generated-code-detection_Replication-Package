class InstancePoolManager:
    """Manager for `InstancePool`"""

    def __init__(self, pool: InstancePool):
        self.pool = pool
        self.instance = None

    def __enter__(self):
        self.instance = self.pool.acquire()
        return self.instance

    def __exit__(self, *_):
        self.pool.release(self.instance)
        self.instance = None