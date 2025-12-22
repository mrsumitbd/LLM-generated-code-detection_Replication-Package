from typing import Any

class _DummyHistogram:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Accept any arguments but ignore them
        pass

    def labels(self, **kwargs: Any) -> "_DummyHistogram":
        # Return self to allow chaining
        return self

    def observe(self, value: float) -> None:
        # No-op: ignore the observed value
        pass

    def time(self) -> "_DummyHistogram":
        # Return self to allow chaining
        return self