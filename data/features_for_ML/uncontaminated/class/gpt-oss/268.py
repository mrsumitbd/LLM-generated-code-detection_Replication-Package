class DummyHook:
    """
    A simple hook implementation that tracks whether it is currently hooked.
    """

    def __init__(self):
        self._hooked = False

    @property
    def is_hooked(self):
        """Return True if the hook is active."""
        return self._hooked

    def hook(self):
        """Activate the hook. Raises RuntimeError if already hooked."""
        if self._hooked:
            raise RuntimeError("Hook is already active.")
        self._hooked = True

    def unhook(self):
        """Deactivate the hook. Raises RuntimeError if not hooked."""
        if not self._hooked:
            raise RuntimeError("Hook is not active.")
        self._hooked = False

    # Optional context manager support
    def __enter__(self):
        self.hook()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unhook()