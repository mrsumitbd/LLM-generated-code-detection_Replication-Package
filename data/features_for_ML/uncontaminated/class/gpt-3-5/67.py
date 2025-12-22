from typing import Any

class _DummyHistogram:

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def labels(self, **kwargs: Any) -> _DummyHistogram:
        pass

    def observe(self, value: float) -> None:
        pass

    def time(self) -> _DummyHistogram:
        pass