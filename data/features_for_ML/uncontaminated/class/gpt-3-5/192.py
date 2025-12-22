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
        return (self._auto_scaling_apply_time + self._pool_update_time +
                self._auto_scaling_submit_time + self._monitor_update_time +
                self._add_tasks_time + self._sleep_time)

    def to_log_string(self) -> str:
        return f"Auto Scaling Apply Time: {self._auto_scaling_apply_time}, " \
               f"Pool Update Time: {self._pool_update_time}, " \
               f"Auto Scaling Submit Time: {self._auto_scaling_submit_time}, " \
               f"Monitor Update Time: {self._monitor_update_time}, " \
               f"Add Tasks Time: {self._add_tasks_time}, " \
               f"Sleep Time: {self._sleep_time}"