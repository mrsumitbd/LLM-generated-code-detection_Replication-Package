class DummySpan:
    """Dummy span class that does nothing when OpenTelemetry is not available."""

    def __init__(self, *args, **kwargs):
        pass

    def end(self, *args, **kwargs):
        pass

    def set_attribute(self, *args, **kwargs):
        pass