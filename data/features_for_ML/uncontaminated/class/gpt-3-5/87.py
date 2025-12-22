class AsyncTask:
    """异步任务基类"""

    def __init__(self, task_name: str | None = None, wait_before_start: int = 0, run_interval: int = 0):
        self.task_name = task_name
        self.wait_before_start = wait_before_start
        self.run_interval = run_interval

    def start(self):
        pass

    def stop(self):
        pass

    def run(self):
        pass