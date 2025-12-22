import threading
import queue

class BackgroundService:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __init__(self):
        self._task_queue = queue.Queue()
        self._running = False
        self._worker_thread = None

    def add_task(self, task_func, *args, **kwargs):
        self._task_queue.put((task_func, args, kwargs))

    def start(self):
        self._running = True
        self._worker_thread = threading.Thread(target=self._process_tasks, daemon=True)
        self._worker_thread.start()

    def _process_tasks(self):
        while self._running:
            try:
                task_func, args, kwargs = self._task_queue.get(block=True, timeout=1)
                task_func(*args, **kwargs)
                self._task_queue.task_done()
            except queue.Empty:
                pass
        self._worker_thread = None