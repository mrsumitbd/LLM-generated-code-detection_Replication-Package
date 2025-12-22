import threading

class BackgroundService:
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.tasks = []
        self.is_running = False

    def add_task(self, task_func, *args, **kwargs):
        self.tasks.append((task_func, args, kwargs))

    def start(self):
        if not self.is_running:
            self.is_running = True
            self._process_tasks()

    def _process_tasks(self):
        if self.tasks:
            task_func, args, kwargs = self.tasks.pop(0)
            threading.Thread(target=task_func, args=args, kwargs=kwargs).start()
            threading.Timer(1, self._process_tasks).start()
        else:
            self.is_running = False