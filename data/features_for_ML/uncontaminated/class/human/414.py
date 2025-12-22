
class DummyBatchSpanProcessor:
    """Dummy implementation of BatchSpanProcessor for when OpenTelemetry is not available."""

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def shutdown(*args, **kwargs):
        pass