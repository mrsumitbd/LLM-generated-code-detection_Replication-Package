from rich.live import Live
from rich.console import Console
from rich.spinner import Spinner

class SpinnerManager:
    def __init__(self, console: Console, message: str = "Processing..."):
        self.console = console
        self.spinner = Spinner("dots", text=message, style="cyan")
        self.live = Live(self.spinner, refresh_per_second=10, console=self.console, transient=True)

    def start(self):
        self.live.start()

    def stop(self):
        self.live.stop()