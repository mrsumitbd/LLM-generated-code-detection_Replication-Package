class ProgressTracker:
    """Advanced progress tracking class."""

    def __init__(self, name: str = "Task"):
        self.name = name
        self.total_steps = 0
        self.completed_steps = 0
        self.progress_percentage = 0.0

    def get_summary(self):
        if self.total_steps == 0:
            return f"{self.name}: 0% complete"
        else:
            self.progress_percentage = (self.completed_steps / self.total_steps) * 100
            return f"{self.name}: {self.progress_percentage:.2f}% complete"

    def add_steps(self, steps: int):
        self.total_steps += steps

    def complete_steps(self, steps: int):
        self.completed_steps += steps
        if self.completed_steps > self.total_steps:
            self.completed_steps = self.total_steps