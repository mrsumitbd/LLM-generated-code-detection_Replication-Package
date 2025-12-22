class HuggingfaceTokenizer:

    def __init__(self, name, seq_len=None, clean=None, **kwargs):
        from transformers import AutoTokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(name, **kwargs)
        self.seq_len = seq_len
        self.clean = clean

    def __call__(self, sequence, **kwargs):
        if self.clean:
            sequence = self._clean(sequence)
        
        encoded = self.tokenizer(
            sequence,
            max_length=self.seq_len,
            padding='max_length' if self.seq_len else False,
            truncation=True if self.seq_len else False,
            return_tensors='pt',
            **kwargs
        )
        
        return encoded

    def _clean(self, text):
        import re
        text = text.lower()
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'http\S+|www\S+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text