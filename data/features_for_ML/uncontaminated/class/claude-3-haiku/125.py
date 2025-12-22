from typing import Any, Dict

class BaseMetric:
    def __init__(self, name: str) -> None:
        self.name = name

    def update(self, value: Any) -> None:
        raise NotImplementedError

    def get_value(self) -> Any:
        raise NotImplementedError

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
        return {name: metric.get_value() for name, metric in self.metrics.items()}

    def reset(self) -> None:
        self.metrics = {}