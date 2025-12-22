import time
import time

class ProgressTracker:
    """Advanced progress tracking class."""

    def __init__(self, name: str = "Task"):
        self.name = name
        self.updates = []
        self.start_time = None

    async def __call__(
        self,
        progress: float,
        total: float = None,
        message: str = None
    ) -> None:
        """Progress callback method."""
        import time
        current_time = time.time()

        if self.start_time is None:
            self.start_time = current_time

        elapsed = current_time - self.start_time

        update = {
            "progress": progress,
            "total": total,
            "message": message,
            "elapsed": elapsed,
            "timestamp": current_time
        }
        self.updates.append(update)

        if total and total > 0:
            percentage = (progress / total) * 100
            print(f"🎯 {self.name}: [{percentage:5.1f}%] {message or 'Processing...'}")
        else:
            print(f"🎯 {self.name}: [Step {progress}] {message or 'Processing...'}")

    def get_summary(self):
        """Get a summary of the progress tracking."""
        if not self.updates:
            return "No progress updates recorded"

        total_time = self.updates[-1]["elapsed"]
        total_updates = len(self.updates)

        return f"""Progress Summary for {self.name}:
- Total updates: {total_updates}
- Total time: {total_time:.2f}s
- Average update interval: {total_time/total_updates:.2f}s
- Final progress: {self.updates[-1]['progress']}/{self.updates[-1]['total']}
"""