
class DatasetMetrics:
    """Aggregated metrics for the entire dataset."""
    total_ref_words: int
    total_correct: int
    total_substitutions: int
    total_deletions: int
    total_insertions: int
    total_ref_chars: int
    total_edit_distance: float
    processed_count: int
    
    @property
    def wer(self) -> float:
        """Calculate Word Error Rate."""
        total_errors = self.total_substitutions + self.total_deletions + self.total_insertions
        return total_errors / max(self.total_ref_words, 1)
    
    @property
    def cer(self) -> float:
        """Calculate Character Error Rate."""
        return self.total_edit_distance / self.total_ref_chars if self.total_ref_chars > 0 else 0.0