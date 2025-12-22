class DummyBatchSpanProcessor:
    """Dummy implementation of BatchSpanProcessor for when OpenTelemetry is not available."""

    def __init__(self, *args, **kwargs):
        # Store arguments for potential debugging or introspection
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def shutdown(*args, **kwargs):
        # No-op shutdown for the dummy processor
        pass