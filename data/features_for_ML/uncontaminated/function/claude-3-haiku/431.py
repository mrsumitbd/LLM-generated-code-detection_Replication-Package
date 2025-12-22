from transformers import BertTokenizer

def init_tokenizer(bert_model_path):
    tokenizer = BertTokenizer.from_pretrained(bert_model_path)
    return tokenizer