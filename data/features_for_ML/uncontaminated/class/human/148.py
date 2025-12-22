from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Generic,
    Iterator,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)
from collections import defaultdict

class MetricManage:
    """MetricManage."""

    def __init__(self):
        """Init metricManage."""
        self.metrics = defaultdict()

    def register_metric(self, cls: Type[EvaluationMetric]):
        """Register metric."""
        self.metrics[cls.name()] = cls

    def get_by_name(self, name: str) -> Type[EvaluationMetric]:
        """Get by name."""
        if name not in self.metrics:
            raise ValueError(f"Metric:{name} not register!")
        return self.metrics[name]

    def all_metric_infos(self):
        """Get all metric infos."""
        result = []
        for name, cls in self.metrics.items():
            result.append(
                {
                    "name": name,
                    "describe": cls.describe,
                }
            )
        return result