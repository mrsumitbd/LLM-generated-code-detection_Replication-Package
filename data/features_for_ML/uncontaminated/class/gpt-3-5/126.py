class TaskStats:
    """Performance statistics for a task"""

    def __init__(self, task_name):
        self.task_name = task_name
        self.total_time = 0
        self.num_executions = 0
        self.avg_time = 0

    def record_execution_time(self, execution_time):
        self.total_time += execution_time
        self.num_executions += 1
        self.avg_time = self.total_time / self.num_executions

    def get_task_name(self):
        return self.task_name

    def get_total_time(self):
        return self.total_time

    def get_num_executions(self):
        return self.num_executions

    def get_avg_time(self):
        return self.avg_time