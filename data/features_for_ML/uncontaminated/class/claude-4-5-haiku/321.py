from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
import threading
import time


class SpinnerManager:

    def __init__(self, console: Console, message: str = "Processing..."):
        self.console = console
        self.message = message
        self.live = None
        self.spinner_thread = None
        self._stop_event = threading.Event()

    def start(self):
        self._stop_event.clear()
        spinner = Spinner("dots", text=self.message)
        self.live = Live(spinner, console=self.console, refresh_per_second=12.5)
        self.live.start()

    def stop(self):
        self._stop_event.set()
        if self.live:
            self.live.stop()
            self.live = None