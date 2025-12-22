class MetricsTracker:
    """Tracks metrics for a single run"""

    def __init__(self) -> None:
        self._metrics: Dict[str, BaseMetric[Any]] = {}

    def add_metric(self, metric: BaseMetric[Any]) -> None:
        self._metrics[metric.name] = metric

    def update(self, name: str, value: Any) -> None:
        if name in self._metrics:
            self._metrics[name].update(value)
        else:
            raise KeyError(f"Metric '{name}' not found in tracker")

    def get_all(self) -> Dict[str, Any]:
        return {name: metric.get() for name, metric in self._metrics.items()}

    def reset(self) -> None:
        for metric in self._metrics.values():
            metric.reset()