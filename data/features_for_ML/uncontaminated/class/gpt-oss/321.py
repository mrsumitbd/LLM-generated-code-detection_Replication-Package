import threading
import time
from typing import Any

class SpinnerManager:
    """
    A simple spinner manager that displays a spinner in the console while a task is running.
    """

    def __init__(self, console: Any, message: str = "Processing..."):
        """
        Parameters
        ----------
        console : Any
            The console object (e.g., rich.console.Console) used to display the spinner.
        message : str, optional
            The message to display next to the spinner. Defaults to "Processing...".
        """
        self.console = console
        self.message = message
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    def start(self):
        """
        Start the spinner in a background thread.
        """
        if self._thread and self._thread.is_alive():
            return  # already running

        self._stop_event.clear()

        def _run_spinner():
            # Use the console's status context manager to show a spinner.
            # The spinner will keep running until the stop event is set.
            with self.console.status(self.message, spinner="dots"):
                while not self._stop_event.is_set():
                    time.sleep(0.1)

        self._thread = threading.Thread(target=_run_spinner, daemon=True)
        self._thread.start()

    def stop(self):
        """
        Stop the spinner and wait for the background thread to finish.
        """
        if not self._thread:
            return

        self._stop_event.set()
        self._thread.join()
        self._thread = None