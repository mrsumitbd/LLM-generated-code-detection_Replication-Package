from typing import Type

class MetricManage:
    """MetricManage."""

    def __init__(self):
        self.metrics = {}

    def register_metric(self, cls: Type[EvaluationMetric]):
        self.metrics[cls.__name__] = cls

    def get_by_name(self, name: str) -> Type[EvaluationMetric]:
        return self.metrics.get(name)

    def all_metric_infos(self):
        return list(self.metrics.keys())