import os
import time
from typing import Tuple, Optional


class CPUMonitor:
    """Non-blocking CPU monitoring with cgroup awareness."""

    def __init__(self, max_cpu_per_core: float):
        self.max_cpu_per_core = max_cpu_per_core
        self._prev_total, self._prev_idle = self._read_proc_stat()
        self._cgroup_limit = self._detect_cgroup_limit()

    def get_cpu_nowait(self) -> float:
        """Return the current CPU usage fraction (0.0–1.0)."""
        total, idle = self._read_proc_stat()
        delta_total = total - self._prev_total
        delta_idle = idle - self._prev_idle
        self._prev_total, self._prev_idle = total, idle

        if delta_total <= 0:
            return 0.0
        usage = (delta_total - delta_idle) / delta_total
        return max(0.0, min(1.0, usage))

    def should_throttle(self) -> bool:
        """Return True if CPU usage exceeds the configured threshold."""
        usage = self.get_cpu_nowait()
        effective_cpus = self._cgroup_limit or os.cpu_count() or 1
        usage_in_cpus = usage * effective_cpus
        threshold = self.max_cpu_per_core * effective_cpus
        return usage_in_cpus > threshold

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _read_proc_stat() -> Tuple[int, int]:
        """Read /proc/stat and return (total_time, idle_time)."""
        try:
            with open("/proc/stat", "r") as f:
                for line in f:
                    if line.startswith("cpu "):
                        parts = line.split()
                        # user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice
                        values = [int(p) for p in parts[1:]]
                        total = sum(values)
                        idle = values[3] + values[4]  # idle + iowait
                        return total, idle
        except Exception:
            pass
        return 0, 0

    @staticmethod
    def _detect_cgroup_limit() -> Optional[float]:
        """Detect cgroup CPU limit (number of cores). Return None if unlimited."""
        # cgroup v2
        cg2_path = "/sys/fs/cgroup/cpu.max"
        if os.path.isfile(cg2_path):
            try:
                with open(cg2_path, "r") as f:
                    line = f.read().strip()
                quota_str, period_str = line.split()
                if quota_str == "max":
                    return None
                quota = int(quota_str)
                period = int(period_str)
                if period > 0:
                    return quota / period
            except Exception:
                pass

        # cgroup v1
        cg1_quota = "/sys/fs/cgroup/cpu/cpu.cfs_quota_us"
        cg1_period = "/sys/fs/cgroup/cpu/cpu.cfs_period_us"
        if os.path.isfile(cg1_quota) and os.path.isfile(cg1_period):
            try:
                with open(cg1_quota, "r") as f:
                    quota = int(f.read().strip())
                with open(cg1_period, "r") as f:
                    period = int(f.read().strip())
                if quota > 0 and period > 0:
                    return quota / period
            except Exception:
                pass

        return None