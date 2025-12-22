import time
from rich.console import Console
from rich.spinner import Spinner

class SpinnerManager:
    def __init__(self, console: Console, message: str = "Processing..."):
        self.console = console
        self.message = message
        self.spinner = Spinner("dots")
        self.spinner_task = None

    def start(self):
        self.spinner_task = self.console.status(self.message, spinner=self.spinner)
        self.spinner_task.__enter__()

    def stop(self):
        self.spinner_task.__exit__(None, None, None)