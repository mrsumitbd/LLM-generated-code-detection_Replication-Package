class _DummyHistogram:

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def labels(self, **kwargs: Any) -> _DummyHistogram:
            return self

        def observe(self, value: float) -> None:
            pass

        def time(self) -> _DummyHistogram:
            return self