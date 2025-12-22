class TaskStats:
    """Performance statistics for a task"""

    def __init__(self):
        self.total_time = 0.0
        self.num_runs = 0
        self.min_time = float('inf')
        self.max_time = 0.0

    def add_run(self, run_time):
        self.total_time += run_time
        self.num_runs += 1
        self.min_time = min(self.min_time, run_time)
        self.max_time = max(self.max_time, run_time)

    @property
    def avg_time(self):
        return self.total_time / self.num_runs if self.num_runs > 0 else 0.0