import threading
import queue
import time


class BackgroundService:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        """
        Return the singleton instance of BackgroundService.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        """
        Initialize the background service.
        """
        # Queue to hold tasks: each item is a tuple (func, args, kwargs)
        self._task_queue = queue.Queue()
        # Event to signal the worker thread to stop
        self._stop_event = threading.Event()
        # Worker thread
        self._worker = threading.Thread(
            target=self._process_tasks, daemon=True
        )
        self._started = False

    def add_task(self, task_func, *args, **kwargs):
        """
        Add a task to the queue.
        """
        if not callable(task_func):
            raise TypeError("task_func must be callable")
        self._task_queue.put((task_func, args, kwargs))

    def start(self):
        """
        Start the background worker thread.
        """
        if not self._started:
            self._worker.start()
            self._started = True

    def _process_tasks(self):
        """
        Worker thread that processes tasks from the queue.
        """
        while not self._stop_event.is_set():
            try:
                # Wait for a task for a short period to allow graceful shutdown
                task_func, args, kwargs = self._task_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                task_func(*args, **kwargs)
            except Exception:
                # Log or ignore exceptions from task execution
                pass
            finally:
                self._task_queue.task_done()

    def stop(self, wait=True):
        """
        Stop the background worker thread.
        """
        self._stop_event.set()
        if wait:
            self._worker.join()