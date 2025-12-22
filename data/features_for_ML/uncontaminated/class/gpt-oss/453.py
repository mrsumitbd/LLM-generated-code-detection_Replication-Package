import datetime
from typing import List, Optional


class ProgressTracker:
    """Advanced progress tracking class."""

    def __init__(self, name: str = "Task"):
        self.name: str = name
        self.total_steps: int = 0
        self.completed_steps: int = 0
        self.steps: List[str] = []
        self.start_time: Optional[datetime.datetime] = None
        self.end_time: Optional[datetime.datetime] = None

    def add_step(self, step_name: str) -> None:
        """Register a new step to be tracked."""
        self.steps.append(step_name)
        self.total_steps += 1

    def complete_step(self) -> None:
        """Mark the next pending step as completed."""
        if self.completed_steps >= self.total_steps:
            raise ValueError("All steps have already been completed.")
        self.completed_steps += 1

    def start(self) -> None:
        """Mark the start time of the task."""
        self.start_time = datetime.datetime.now()

    def finish(self) -> None:
        """Mark the end time of the task."""
        self.end_time = datetime.datetime.now()

    def get_summary(self) -> str:
        """Return a human‑readable summary of the current progress."""
        percent = (
            (self.completed_steps / self.total_steps) * 100
            if self.total_steps > 0
            else 0.0
        )
        elapsed_seconds: Optional[float] = None
        if self.start_time:
            end = self.end_time or datetime.datetime.now()
            elapsed_seconds = (end - self.start_time).total_seconds()

        lines = [
            f"Task: {self.name}",
            f"Completed {self.completed_steps}/{self.total_steps} steps "
            f"({percent:.2f}%)",
        ]
        if elapsed_seconds is not None:
            lines.append(f"Elapsed time: {elapsed_seconds:.2f} seconds")
        return "\n".join(lines)