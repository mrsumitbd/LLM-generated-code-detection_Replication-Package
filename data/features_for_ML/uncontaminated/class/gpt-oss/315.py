class ControlSignal:
    def __init__(self) -> None:
        self._in_loop: bool = False

    def start(self) -> None:
        """Signal that a loop has started."""
        self._in_loop = True

    def stop(self) -> None:
        """Signal that a loop has stopped."""
        self._in_loop = False

    def is_in_loop(self) -> bool:
        """Return True if the loop is currently running, False otherwise."""
        return self._in_loop