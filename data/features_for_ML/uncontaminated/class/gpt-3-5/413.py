class SchedulerService:
    """Service for managing scheduled tasks and automatic execution"""

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def execute_tasks(self):
        for task in self.tasks:
            task.execute()

class Task:
    def __init__(self, name):
        self.name = name

    def execute(self):
        print(f"Executing task: {self.name}")

# Example usage:
scheduler = SchedulerService()
task1 = Task("Task 1")
task2 = Task("Task 2")

scheduler.add_task(task1)
scheduler.add_task(task2)

scheduler.execute_tasks()