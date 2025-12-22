from typing import Type, Dict, List, Tuple

class MetricManage:
    """MetricManage."""

    def __init__(self):
        self._metrics: Dict[str, Type] = {}

    def register_metric(self, cls: Type):
        """Register a metric class.

        Args:
            cls: The metric class to register. It must have a unique name
                 accessible via `cls.__name__`.

        Raises:
            ValueError: If a metric with the same name is already registered.
        """
        name = cls.__name__
        if name in self._metrics:
            raise ValueError(f"Metric '{name}' is already registered.")
        self._metrics[name] = cls

    def get_by_name(self, name: str) -> Type:
        """Retrieve a registered metric class by its name.

        Args:
            name: The name of the metric class.

        Returns:
            The metric class associated with the given name.

        Raises:
            KeyError: If no metric with the given name is registered.
        """
        return self._metrics[name]

    def all_metric_infos(self) -> List[Tuple[str, Type]]:
        """Return a list of all registered metric names and their classes.

        Returns:
            A list of tuples (name, class) for each registered metric.
        """
        return list(self._metrics.items())