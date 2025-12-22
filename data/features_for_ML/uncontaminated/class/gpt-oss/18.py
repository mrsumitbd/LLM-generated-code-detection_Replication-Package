class DatasetMetrics:
    """Aggregated metrics for the entire dataset."""

    def __init__(self, metrics=None):
        """
        Parameters
        ----------
        metrics : Iterable[tuple[float, float]] or None
            Optional initial list of (wer, cer) tuples.
        """
        self._metrics = list(metrics) if metrics is not None else []

    def add(self, wer: float, cer: float) -> None:
        """Add a new (wer, cer) pair to the dataset."""
        self._metrics.append((wer, cer))

    @property
    def wer(self) -> float:
        """Average word error rate over all added samples."""
        if not self._metrics:
            return 0.0
        return sum(m[0] for m in self._metrics) / len(self._metrics)

    @property
    def cer(self) -> float:
        """Average character error rate over all added samples."""
        if not self._metrics:
            return 0.0
        return sum(m[1] for m in self._metrics) / len(self._metrics)

    def __repr__(self) -> str:
        return f"<DatasetMetrics wer={self.wer:.4f} cer={self.cer:.4f} samples={len(self._metrics)}>"