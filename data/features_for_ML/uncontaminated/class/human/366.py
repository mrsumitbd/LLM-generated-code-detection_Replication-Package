
class DummySpanExporter:
    """Dummy span exporter that does nothing."""

    @staticmethod
    def export(*args, **kwargs):
        pass

    @staticmethod
    def shutdown(*args, **kwargs):
        pass