from typing import Any, Dict

class MetricsTracker:
    """Tracks metrics for a single run"""

    def __init__(self) -> None:
        self._metrics: Dict[str, BaseMetric[Any]] = {}

    def add_metric(self, metric: BaseMetric[Any]) -> None:
        """Add a metric to the tracker."""
        self._metrics[metric.name] = metric

    def update(self, name: str, value: Any) -> None:
        """Update a specific metric by name."""
        if name not in self._metrics:
            raise KeyError(f"Metric '{name}' not found.")
        self._metrics[name].update(value)

    def get_all(self) -> Dict[str, Any]:
        """Return a dictionary of all metric values."""
        return {name: metric.get_value() for name, metric in self._metrics.items()}

    def reset(self) -> None:
        """Reset all metrics."""
        for metric in self._metrics.values():
            metric.reset()