import datetime
import threading
import time

class SchedulerService:
    """Service for managing scheduled tasks and automatic execution"""

    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.thread.start()

    def add_task(self, task, schedule_time):
        with self.lock:
            self.tasks.append((task, schedule_time))

    def remove_task(self, task):
        with self.lock:
            self.tasks = [(t, st) for t, st in self.tasks if t != task]

    def run_scheduler(self):
        while True:
            with self.lock:
                now = datetime.datetime.now()
                for task, schedule_time in self.tasks[:]:
                    if schedule_time <= now:
                        try:
                            task()
                        except Exception as e:
                            print(f"Error executing task: {e}")
                        self.tasks.remove((task, schedule_time))
            time.sleep(1)