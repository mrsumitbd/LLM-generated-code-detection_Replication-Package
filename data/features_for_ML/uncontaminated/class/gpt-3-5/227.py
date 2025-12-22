import time

class TimerService:
    """
    Timer service that manages all countdown tasks.
    """

    def __init__(self):
        self.tasks = []

    def add_task(self, task_name, duration):
        self.tasks.append((task_name, duration))

    def run_tasks(self):
        for task_name, duration in self.tasks:
            print(f"Starting task: {task_name}")
            time.sleep(duration)
            print(f"Task {task_name} completed")

# Example usage:
timer_service = TimerService()
timer_service.add_task("Task 1", 5)
timer_service.add_task("Task 2", 3)
timer_service.run_tasks()