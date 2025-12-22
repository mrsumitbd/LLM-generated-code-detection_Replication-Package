
class StreamingExecutorTiming:
    iteration_start: float = 0.0
    auto_scaling_apply_end: float = 0.0
    pool_update_end: float = 0.0
    auto_scaling_submit_end: float = 0.0
    monitor_update_end: float = 0.0
    add_tasks_end: float = 0.0
    sleep_end: float = 0.0

    @property
    def auto_scaling_apply_time(self) -> float:
        return self.auto_scaling_apply_end - self.iteration_start

    @property
    def pool_update_time(self) -> float:
        return self.pool_update_end - self.auto_scaling_apply_end

    @property
    def auto_scaling_submit_time(self) -> float:
        return self.auto_scaling_submit_end - self.pool_update_end

    @property
    def monitor_update_time(self) -> float:
        return self.monitor_update_end - self.auto_scaling_submit_end

    @property
    def add_tasks_time(self) -> float:
        return self.add_tasks_end - self.monitor_update_end

    @property
    def sleep_time(self) -> float:
        return self.sleep_end - self.add_tasks_end

    @property
    def total_time(self) -> float:
        return self.sleep_end - self.iteration_start

    def to_log_string(self) -> str:
        stages: list[tuple[str, float]] = [
            ("Auto Scaling Apply", self.auto_scaling_apply_time),
            ("Pool Update", self.pool_update_time),
            ("Auto Scaling Submit", self.auto_scaling_submit_time),
            ("Monitor Update", self.monitor_update_time),
            ("Add Tasks", self.add_tasks_time),
            ("Sleep", self.sleep_time),
            ("Total", self.total_time),
        ]

        log_lines = ["StreamingExecutor Timing Summary:"]
        max_name_length = max(len(name) for name, _ in stages)

        for name, duration in stages:
            log_lines.append(f"  {name:<{max_name_length}}: {duration:.6f} seconds")

        return "\n".join(log_lines)