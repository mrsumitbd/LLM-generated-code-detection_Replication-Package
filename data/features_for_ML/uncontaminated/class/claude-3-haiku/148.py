from typing import Type, Dict

class EvaluationMetric:
    """Base class for evaluation metrics."""
    name: str
    description: str

class MetricManage:
    """MetricManage."""

    def __init__(self):
        self._registered_metrics: Dict[str, Type[EvaluationMetric]] = {}

    def register_metric(self, cls: Type[EvaluationMetric]):
        self._registered_metrics[cls.name] = cls

    def get_by_name(self, name: str) -> Type[EvaluationMetric]:
        return self._registered_metrics[name]

    def all_metric_infos(self):
        return list(self._registered_metrics.values())