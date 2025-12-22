class StreamingExecutorTiming:
    def __init__(self):
        self._auto_scaling_apply_time = 0.0
        self._pool_update_time = 0.0
        self._auto_scaling_submit_time = 0.0
        self._monitor_update_time = 0.0
        self._add_tasks_time = 0.0
        self._sleep_time = 0.0

    @property
    def auto_scaling_apply_time(self) -> float:
        return self._auto_scaling_apply_time

    @auto_scaling_apply_time.setter
    def auto_scaling_apply_time(self, value: float):
        self._auto_scaling_apply_time = value

    @property
    def pool_update_time(self) -> float:
        return self._pool_update_time

    @pool_update_time.setter
    def pool_update_time(self, value: float):
        self._pool_update_time = value

    @property
    def auto_scaling_submit_time(self) -> float:
        return self._auto_scaling_submit_time

    @auto_scaling_submit_time.setter
    def auto_scaling_submit_time(self, value: float):
        self._auto_scaling_submit_time = value

    @property
    def monitor_update_time(self) -> float:
        return self._monitor_update_time

    @monitor_update_time.setter
    def monitor_update_time(self, value: float):
        self._monitor_update_time = value

    @property
    def add_tasks_time(self) -> float:
        return self._add_tasks_time

    @add_tasks_time.setter
    def add_tasks_time(self, value: float):
        self._add_tasks_time = value

    @property
    def sleep_time(self) -> float:
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, value: float):
        self._sleep_time = value

    @property
    def total_time(self) -> float:
        return (
            self._auto_scaling_apply_time
            + self._pool_update_time
            + self._auto_scaling_submit_time
            + self._monitor_update_time
            + self._add_tasks_time
            + self._sleep_time
        )

    def to_log_string(self) -> str:
        return (
            f"auto_scaling_apply_time: {self._auto_scaling_apply_time:.3f}s, "
            f"pool_update_time: {self._pool_update_time:.3f}s, "
            f"auto_scaling_submit_time: {self._auto_scaling_submit_time:.3f}s, "
            f"monitor_update_time: {self._monitor_update_time:.3f}s, "
            f"add_tasks_time: {self._add_tasks_time:.3f}s, "
            f"sleep_time: {self._sleep_time:.3f}s, "
            f"total_time: {self.total_time:.3f}s"
        )