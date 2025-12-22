class DummySpan:
    """Dummy span class that does nothing when OpenTelemetry is not available."""

    def __init__(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass

    def set_attribute(self, *args, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
        return False  # propagate exceptions if any