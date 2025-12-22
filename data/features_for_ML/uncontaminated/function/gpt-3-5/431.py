def init_tokenizer(bert_model_path):
    from transformers import BertTokenizer
    tokenizer = BertTokenizer.from_pretrained(bert_model_path)
    return tokenizer