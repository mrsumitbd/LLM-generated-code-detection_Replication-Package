import re

class HuggingfaceTokenizer:
    def __init__(self, name, seq_len=None, clean=None, **kwargs):
        self.name = name
        self.seq_len = seq_len
        self.clean = clean if clean else self._clean
        self.tokenizer = self._load_tokenizer(name, **kwargs)

    def __call__(self, sequence, **kwargs):
        cleaned_sequence = self.clean(sequence)
        return self.tokenizer(cleaned_sequence, max_length=self.seq_len, padding='max_length', truncation=True, **kwargs)

    def _clean(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower().strip()

    def _load_tokenizer(self, name, **kwargs):
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained(name, **kwargs)