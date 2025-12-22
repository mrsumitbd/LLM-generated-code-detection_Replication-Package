from transformers import BertTokenizer

def init_tokenizer(bert_model_path):
    tokenizer = BertTokenizer.from_pretrained(bert_model_path)
    tokenizer.add_special_tokens({'bos_token':'[DEC]'})
    tokenizer.add_special_tokens({'additional_special_tokens':['[ENC]']})       
    tokenizer.enc_token_id = tokenizer.additional_special_tokens_ids[0]  
    return tokenizer