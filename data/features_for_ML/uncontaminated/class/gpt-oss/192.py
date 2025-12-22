class StreamingExecutorTiming:
    def __init__(
        self,
        auto_scaling_apply_time: float = 0.0,
        pool_update_time: float = 0.0,
        auto_scaling_submit_time: float = 0.0,
        monitor_update_time: float = 0.0,
        add_tasks_time: float = 0.0,
        sleep_time: float = 0.0,
    ) -> None:
        self._auto_scaling_apply_time = float(auto_scaling_apply_time)
        self._pool_update_time = float(pool_update_time)
        self._auto_scaling_submit_time = float(auto_scaling_submit_time)
        self._monitor_update_time = float(monitor_update_time)
        self._add_tasks_time = float(add_tasks_time)
        self._sleep_time = float(sleep_time)

    @property
    def auto_scaling_apply_time(self) -> float:
        return self._auto_scaling_apply_time

    @property
    def pool_update_time(self) -> float:
        return self._pool_update_time

    @property
    def auto_scaling_submit_time(self) -> float:
        return self._auto_scaling_submit_time

    @property
    def monitor_update_time(self) -> float:
        return self._monitor_update_time

    @property
    def add_tasks_time(self) -> float:
        return self._add_tasks_time

    @property
    def sleep_time(self) -> float:
        return self._sleep_time

    @property
    def total_time(self) -> float:
        return (
            self.auto_scaling_apply_time
            + self.pool_update_time
            + self.auto_scaling_submit_time
            + self.monitor_update_time
            + self.add_tasks_time
            + self.sleep_time
        )

    def to_log_string(self) -> str:
        return (
            f"StreamingExecutorTiming("
            f"auto_scaling_apply_time={self.auto_scaling_apply_time:.6f}, "
            f"pool_update_time={self.pool_update_time:.6f}, "
            f"auto_scaling_submit_time={self.auto_scaling_submit_time:.6f}, "
            f"monitor_update_time={self.monitor_update_time:.6f}, "
            f"add_tasks_time={self.add_tasks_time:.6f}, "
            f"sleep_time={self.sleep_time:.6f}, "
            f"total_time={self.total_time:.6f})"
        )