import os
from transformers import AutoTokenizer

def init_tokenizer(bert_model_path):
    """Initialize a tokenizer from a BERT model path."""
    if not os.path.exists(bert_model_path):
        raise FileNotFoundError(f"Model path does not exist: {bert_model_path}")
    
    tokenizer = AutoTokenizer.from_pretrained(bert_model_path)
    return tokenizer