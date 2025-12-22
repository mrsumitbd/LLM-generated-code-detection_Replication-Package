
class InstancePoolManager:
    """Manager for `InstancePool`"""

    def __init__(self, pool: InstancePool):
        """Initialize a new InstancePoolManager. This object will handle enter/exit hooks during a `with` clause
        Args:
            pool (InstancePool): The InstancePool to interact with
        """

        self.pool = pool
        self.obj = None

    def __enter__(self):
        """User-code has entered `with` clause, acquire Shotgun instance"""

        self.instance = self.pool.acquire()
        logger.debug(
            f"Manager: Allocated Shotgun instance with ID {id(self.instance)} (session token {self.instance.config.session_token})"
        )

        return self.instance

    def __exit__(self, *_):
        """User-code has exited `with` clause, release Shotgun instance"""

        self.pool.release(self.instance)