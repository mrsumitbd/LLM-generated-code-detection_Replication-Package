class ProgressTracker:
    """Advanced progress tracking class."""

    def __init__(self, name: str = "Task"):
        self.name = name
        self.total_steps = 0
        self.completed_steps = 0

    def get_summary(self):
        return f"{self.name}: {self.completed_steps}/{self.total_steps} steps completed"