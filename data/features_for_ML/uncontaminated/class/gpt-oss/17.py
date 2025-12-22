import threading
import time
from typing import Any


class DebeziumJsonEngine:
    """
    Main class to manage the Debezium embedded engine.
    """

    def __init__(self, properties: Any, handler: Any):
        """
        Initialize the Debezium engine with the given properties and change handler.

        :param properties: Configuration properties for the Debezium engine.
        :param handler: An instance of BasePythonChangeHandler that will process change events.
        """
        self.properties = properties
        self.handler = handler
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def run(self):
        """
        Start the Debezium engine in a background thread.
        """
        if self._thread and self._thread.is_alive():
            return  # already running
        self._thread = threading.Thread(target=self._run_engine, daemon=True)
        self._thread.start()

    def interrupt(self):
        """
        Signal the Debezium engine to stop and wait for the thread to finish.
        """
        self._stop_event.set()
        if self._thread:
            self._thread.join()

    def _run_engine(self):
        """
        Internal method that simulates the Debezium engine loop.
        It repeatedly generates a dummy change event and passes it to the handler.
        """
        while not self._stop_event.is_set():
            # Simulate a change event (this would normally come from Debezium)
            change_event = {
                "op": "c",
                "ts_ms": int(time.time() * 1000),
                "before": None,
                "after": {"id": 1, "name": "Alice"},
            }
            try:
                self.handler.handle_change(change_event)
            except Exception:
                # In a real implementation, proper error handling would be required
                pass
            time.sleep(1)