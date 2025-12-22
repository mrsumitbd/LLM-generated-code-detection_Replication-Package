class ControlSignal:
    def __init__(self) -> None:
        self._is_in_loop = False

    def start(self) -> None:
        self._is_in_loop = True

    def stop(self) -> None:
        self._is_in_loop = False

    def is_in_loop(self) -> bool:
        return self._is_in_loop