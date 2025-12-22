from dataclasses import dataclass, field
from typing import Any, Dict, Generic, Optional, Type, TypeVar

class MetricsTracker:
    """Tracks metrics for a single run"""

    metrics: Dict[str, BaseMetric[Any]] = field(default_factory=dict)

    def add_metric(self, metric: BaseMetric[Any]) -> None:
        """Add a metric to track"""
        self.metrics[metric.name] = metric

    def update(self, name: str, value: Any) -> None:
        """Update a metric value"""
        if name in self.metrics:
            self.metrics[name].update(value)

    def get_all(self) -> Dict[str, Any]:
        """Get all metric values"""
        return {
            name: {
                'value': metric.get_value(),
                'unit': metric.unit,
                'description': metric.description,
            }
            for name, metric in self.metrics.items()
        }

    def reset(self) -> None:
        """Reset all metrics"""
        for metric in self.metrics.values():
            metric.reset()