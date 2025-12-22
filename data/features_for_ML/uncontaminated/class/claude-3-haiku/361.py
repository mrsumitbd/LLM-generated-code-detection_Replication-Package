class WorkerRunData:
    def __init__(self, worker_id, start_time, end_time, status):
        self.worker_id = worker_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self._stopped = False

    def _to_print_key(self):
        return f"{self.worker_id}_{self.start_time}"

    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, value):
        self._stopped = value