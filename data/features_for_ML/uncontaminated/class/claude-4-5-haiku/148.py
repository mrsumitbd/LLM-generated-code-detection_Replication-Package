class MetricManage:
    """MetricManage."""

    def __init__(self):
        self._metrics = {}

    def register_metric(self, cls: Type[EvaluationMetric]):
        if not hasattr(cls, 'name') or cls.name is None:
            raise ValueError(f"Metric class {cls.__name__} must have a 'name' attribute")
        self._metrics[cls.name] = cls

    def get_by_name(self, name: str) -> Type[EvaluationMetric]:
        if name not in self._metrics:
            raise KeyError(f"Metric '{name}' not found. Available metrics: {list(self._metrics.keys())}")
        return self._metrics[name]

    def all_metric_infos(self):
        return list(self._metrics.values())