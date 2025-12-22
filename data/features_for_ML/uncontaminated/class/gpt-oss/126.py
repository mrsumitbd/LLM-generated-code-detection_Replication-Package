import time
import tracemalloc
from collections import defaultdict
from typing import Any, Dict, Optional


class TaskStats:
    """Performance statistics for a task."""

    def __init__(self, name: Optional[str] = None):
        self.name: Optional[str] = name
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.duration: Optional[float] = None
        self.metrics: Dict[str, Any] = {}
        self._running: bool = False
        self._memory_start: Optional[int] = None
        self._memory_peak: Optional[int] = None

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------
    def start(self) -> None:
        if self._running:
            raise RuntimeError("Task already started")
        self.start_time = time.perf_counter()
        self._running = True
        self._memory_start = tracemalloc.get_traced_memory()[0]
        self._memory_peak = tracemalloc.get_traced_memory()[1]

    def stop(self) -> None:
        if not self._running:
            raise RuntimeError("Task not started")
        self.end_time = time.perf_counter()
        self.duration = self.end_time - self.start_time
        self._running = False
        current, peak = tracemalloc.get_traced_memory()
        self._memory_peak = max(self._memory_peak or 0, peak)
        self.add_metric("memory_peak_bytes", self._memory_peak)

    @property
    def elapsed(self) -> Optional[float]:
        """Return elapsed time if the task has been stopped."""
        return self.duration

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------
    def add_metric(self, key: str, value: Any) -> None:
        self.metrics[key] = value

    def get_metric(self, key: str, default: Any = None) -> Any:
        return self.metrics.get(key, default)

    def merge(self, other: "TaskStats") -> None:
        """Merge another TaskStats into this one."""
        if other.duration is not None:
            if self.duration is None:
                self.duration = other.duration
            else:
                self.duration += other.duration
        self.metrics.update(other.metrics)

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "TaskStats":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.stop()
        return False  # propagate exceptions

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def reset(self) -> None:
        """Reset all statistics."""
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.metrics.clear()
        self._running = False
        self._memory_start = None
        self._memory_peak = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "metrics": dict(self.metrics),
        }

    def __repr__(self) -> str:
        dur = f"{self.duration:.6f}s" if self.duration is not None else "N/A"
        return f"<TaskStats name={self.name!r} duration={dur} metrics={self.metrics}>"