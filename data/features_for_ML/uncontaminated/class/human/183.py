from ...utils.logger import logger
import threading

class BackgroundService:

    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = BackgroundService()
        return cls._instance
    
    def __init__(self):
        self.tasks = []
        self.is_running = False
        self.worker_thread = None
    
    def add_task(self, task_func, *args, **kwargs):
        self.tasks.append((task_func, args, kwargs))
        logger.info(f"Added background task: {task_func.__name__}")
        
        if not self.is_running:
            self.start()
    
    def start(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._process_tasks, daemon=False)
        self.worker_thread.start()
        logger.info("Background service started")
    
    def _process_tasks(self):
        while self.tasks:
            task_func, args, kwargs = self.tasks.pop(0)
            try:
                logger.info(f"Executing background task: {task_func.__name__}")
                task_func(*args, **kwargs)
                logger.info(f"Background task completed: {task_func.__name__}")
            except Exception as e:
                logger.error(f"Background task execution failed: {e}")
        
        logger.info("All background tasks completed, service stopped")
        self.is_running = False