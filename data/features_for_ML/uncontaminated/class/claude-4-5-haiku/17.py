from typing import Optional
import threading
import time
from abc import ABC, abstractmethod


class Properties(dict):
    """Properties dictionary wrapper"""
    pass


class BasePythonChangeHandler(ABC):
    """Base class for change handlers"""
    @abstractmethod
    def handle_record(self, record):
        pass


class DebeziumJsonEngine:
    """
    Main class to manage the Debezium embedded engine.
    """

    def __init__(self, properties: Properties, handler: BasePythonChangeHandler):
        self.properties = properties
        self.handler = handler
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def run(self):
        """Start the Debezium engine in a separate thread"""
        if self._running:
            raise RuntimeError("Engine is already running")
        
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_engine, daemon=False)
        self._thread.start()

    def _run_engine(self):
        """Internal method to run the engine loop"""
        try:
            while self._running and not self._stop_event.is_set():
                # Simulate engine processing
                # In a real implementation, this would interact with Debezium
                time.sleep(0.1)
        except Exception as e:
            self._running = False
            raise
        finally:
            self._running = False

    def interrupt(self):
        """Stop the Debezium engine"""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)