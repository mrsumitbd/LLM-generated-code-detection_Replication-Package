class CPUMonitor:
    """Non-blocking CPU monitoring with cgroup awareness."""

    def __init__(self, max_cpu_per_core: float):
        self.max_cpu_per_core = max_cpu_per_core

    def get_cpu_nowait(self) -> float:
        # Placeholder implementation to return a random CPU usage value
        import random
        return random.uniform(0, 100)

    def should_throttle(self) -> bool:
        cpu_usage = self.get_cpu_nowait()
        return cpu_usage > self.max_cpu_per_core