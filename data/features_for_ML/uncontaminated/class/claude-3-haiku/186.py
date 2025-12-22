import psutil
import os

class CPUMonitor:
    """Non-blocking CPU monitoring with cgroup awareness."""

    def __init__(self, max_cpu_per_core: float):
        self.max_cpu_per_core = max_cpu_per_core
        self.cgroup_path = self._get_cgroup_path()
        self.cpu_count = psutil.cpu_count(logical=True)
        self.cpu_usage_history = [0.0] * self.cpu_count

    def _get_cgroup_path(self):
        try:
            with open('/proc/self/cgroup', 'r') as f:
                for line in f:
                    if 'cpu' in line:
                        return line.split(':')[2].strip()
        except FileNotFoundError:
            return None

    def get_cpu_nowait(self) -> float:
        if self.cgroup_path:
            with open(f'{self.cgroup_path}/cpu.usage', 'r') as f:
                cpu_usage = float(f.read().strip())
            self.cpu_usage_history.pop(0)
            self.cpu_usage_history.append(cpu_usage / (10 ** 9 * self.cpu_count))
            return sum(self.cpu_usage_history) / len(self.cpu_usage_history)
        else:
            return sum(psutil.cpu_percent(interval=None, percpu=True)) / self.cpu_count

    def should_throttle(self) -> bool:
        return self.get_cpu_nowait() >= self.max_cpu_per_core