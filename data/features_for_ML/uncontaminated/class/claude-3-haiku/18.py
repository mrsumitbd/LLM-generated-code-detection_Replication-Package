class DatasetMetrics:
    """Aggregated metrics for the entire dataset."""

    def __init__(self, wer: float, cer: float):
        self._wer = wer
        self._cer = cer

    @property
    def wer(self) -> float:
        return self._wer

    @property
    def cer(self) -> float:
        return self._cer