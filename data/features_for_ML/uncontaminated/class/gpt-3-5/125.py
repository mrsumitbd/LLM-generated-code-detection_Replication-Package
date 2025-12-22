from typing import Any, Dict
from base_metric import BaseMetric

class MetricsTracker:
    """Tracks metrics for a single run"""

    def __init__(self):
        self.metrics = {}

    def add_metric(self, metric: BaseMetric[Any]) -> None:
        self.metrics[metric.name] = metric

    def update(self, name: str, value: Any) -> None:
        if name in self.metrics:
            self.metrics[name].update(value)

    def get_all(self) -> Dict[str, Any]:
        return {name: metric.value for name, metric in self.metrics.items()}

    def reset(self) -> None:
        for metric in self.metrics.values():
            metric.reset()