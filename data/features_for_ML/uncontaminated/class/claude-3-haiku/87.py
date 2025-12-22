class AsyncTask:
    """异步任务基类"""

    def __init__(self, task_name: str | None = None, wait_before_start: int = 0, run_interval: int = 0):
        self.task_name = task_name
        self.wait_before_start = wait_before_start
        self.run_interval = run_interval
        self.is_running = False
        self.task_thread = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.task_thread = threading.Thread(target=self.run)
            self.task_thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.task_thread.join()

    def run(self):
        time.sleep(self.wait_before_start)
        while self.is_running:
            self.execute()
            time.sleep(self.run_interval)

    def execute(self):
        raise NotImplementedError("Subclasses must implement the execute method")