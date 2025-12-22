class WorkerRunData:
    """
    Holds runtime information for a worker instance.
    """

    def __init__(self, worker_id, worker_name, start_time=None, end_time=None):
        """
        Initialize a new WorkerRunData instance.

        :param worker_id: Unique identifier for the worker.
        :param worker_name: Human‑readable name of the worker.
        :param start_time: Timestamp when the worker started (optional).
        :param end_time: Timestamp when the worker finished (optional).
        """
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.start_time = start_time
        self.end_time = end_time
        self._stopped = False

    def _to_print_key(self):
        """
        Return a concise key used for logging or debugging.

        The key is a combination of the worker's ID and name.
        """
        return f"{self.worker_id}:{self.worker_name}"

    @property
    def stopped(self):
        """
        Indicates whether the worker has stopped.

        The worker is considered stopped if either the internal flag
        `_stopped` is True or an `end_time` has been recorded.
        """
        return self._stopped or self.end_time is not None

    # Optional helper to mark the worker as stopped
    def stop(self, end_time=None):
        """
        Mark the worker as stopped and optionally record an end time.

        :param end_time: Timestamp when the worker stopped (optional).
        """
        self._stopped = True
        if end_time is not None:
            self.end_time = end_time