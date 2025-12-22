from typing import Any

class _DummyHistogram:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self._labels = {}
        self._values = []

    def labels(self, **kwargs: Any) -> "_DummyHistogram":
        self._labels.update(kwargs)
        return self

    def observe(self, value: float) -> None:
        self._values.append(value)

    def time(self) -> "_DummyHistogram":
        return self