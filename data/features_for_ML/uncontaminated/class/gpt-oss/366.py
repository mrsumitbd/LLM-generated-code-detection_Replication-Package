class DummySpanExporter:
    """Dummy span exporter that does nothing."""

    @staticmethod
    def export(*args, **kwargs):
        # No-op export
        return None

    @staticmethod
    def shutdown(*args, **kwargs):
        # No-op shutdown
        return None