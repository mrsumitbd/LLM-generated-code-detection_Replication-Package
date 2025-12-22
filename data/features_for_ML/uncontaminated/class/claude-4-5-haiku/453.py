class ProgressTracker:
    """Advanced progress tracking class."""

    def __init__(self, name: str = "Task"):
        self.name = name
        self.total_steps = 0
        self.completed_steps = 0
        self.start_time = None
        self.end_time = None
        self.status = "not_started"
        self.history = []

    def start(self):
        """Start the progress tracking."""
        import time
        self.start_time = time.time()
        self.status = "in_progress"
        self.history.append({"event": "started", "time": self.start_time})

    def set_total_steps(self, total: int):
        """Set the total number of steps."""
        self.total_steps = total

    def update(self, steps: int = 1):
        """Update progress by incrementing completed steps."""
        self.completed_steps = min(self.completed_steps + steps, self.total_steps)
        if self.completed_steps == self.total_steps and self.total_steps > 0:
            self.status = "completed"

    def complete(self):
        """Mark the task as completed."""
        import time
        self.end_time = time.time()
        self.completed_steps = self.total_steps
        self.status = "completed"
        self.history.append({"event": "completed", "time": self.end_time})

    def get_progress_percentage(self) -> float:
        """Get the progress as a percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.completed_steps / self.total_steps) * 100

    def get_elapsed_time(self) -> float:
        """Get the elapsed time in seconds."""
        import time
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time is not None else time.time()
        return end - self.start_time

    def get_summary(self):
        """Get a summary of the progress."""
        summary = {
            "name": self.name,
            "status": self.status,
            "total_steps": self.total_steps,
            "completed_steps": self.completed_steps,
            "progress_percentage": self.get_progress_percentage(),
            "elapsed_time": self.get_elapsed_time(),
            "history": self.history
        }
        return summary

    def reset(self):
        """Reset the progress tracker."""
        self.completed_steps = 0
        self.start_time = None
        self.end_time = None
        self.status = "not_started"
        self.history = []

    def __str__(self) -> str:
        """String representation of the progress tracker."""
        percentage = self.get_progress_percentage()
        return f"{self.name}: {self.completed_steps}/{self.total_steps} ({percentage:.1f}%) - {self.status}"