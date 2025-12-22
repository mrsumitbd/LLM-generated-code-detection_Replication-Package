class ControlSignal:

    def __init__(self) -> None:
        self._running = False

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def is_in_loop(self) -> bool:
        return self._running