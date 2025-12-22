class HuggingfaceTokenizer:

    def __init__(self, name, seq_len=None, clean=None, **kwargs):
        self.name = name
        self.seq_len = seq_len
        self.clean = clean

    def __call__(self, sequence, **kwargs):
        if self.clean:
            sequence = self._clean(sequence)
        return sequence

    def _clean(self, text):
        # Implement text cleaning logic here
        cleaned_text = text.lower().strip()
        return cleaned_text