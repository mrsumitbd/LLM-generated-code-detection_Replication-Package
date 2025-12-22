class DatasetMetrics:
    """Aggregated metrics for the entire dataset."""

    def __init__(self, total_words: int = 0, word_errors: int = 0, 
                 total_chars: int = 0, char_errors: int = 0):
        self.total_words = total_words
        self.word_errors = word_errors
        self.total_chars = total_chars
        self.char_errors = char_errors

    @property
    def wer(self) -> float:
        """Word Error Rate: word_errors / total_words"""
        if self.total_words == 0:
            return 0.0
        return self.word_errors / self.total_words

    @property
    def cer(self) -> float:
        """Character Error Rate: char_errors / total_chars"""
        if self.total_chars == 0:
            return 0.0
        return self.char_errors / self.total_chars