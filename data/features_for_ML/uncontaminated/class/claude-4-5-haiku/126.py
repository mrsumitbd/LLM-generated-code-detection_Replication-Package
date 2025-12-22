class TaskStats:
    """Performance statistics for a task"""
    
    def __init__(self):
        self.total_time = 0.0
        self.call_count = 0
        self.min_time = float('inf')
        self.max_time = 0.0
        self.errors = 0
    
    def record_execution(self, execution_time, error=False):
        """Record a task execution"""
        self.total_time += execution_time
        self.call_count += 1
        self.min_time = min(self.min_time, execution_time)
        self.max_time = max(self.max_time, execution_time)
        if error:
            self.errors += 1
    
    def get_average_time(self):
        """Get average execution time"""
        if self.call_count == 0:
            return 0.0
        return self.total_time / self.call_count
    
    def get_success_rate(self):
        """Get success rate as percentage"""
        if self.call_count == 0:
            return 100.0
        return ((self.call_count - self.errors) / self.call_count) * 100
    
    def reset(self):
        """Reset all statistics"""
        self.total_time = 0.0
        self.call_count = 0
        self.min_time = float('inf')
        self.max_time = 0.0
        self.errors = 0
    
    def __str__(self):
        """String representation of statistics"""
        if self.call_count == 0:
            return "TaskStats(no executions)"
        return (f"TaskStats(calls={self.call_count}, avg={self.get_average_time():.4f}s, "
                f"min={self.min_time:.4f}s, max={self.max_time:.4f}s, "
                f"errors={self.errors}, success_rate={self.get_success_rate():.2f}%)")
    
    def __repr__(self):
        """Representation of statistics"""
        return self.__str__()