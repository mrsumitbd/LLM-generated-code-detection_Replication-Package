import threading

class ControlSignal:
    def __init__(self) -> None:
        self._running = False
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            self._running = True

    def stop(self) -> None:
        with self._lock:
            self._running = False

    def is_in_loop(self) -> bool:
        with self._lock:
            return self._running