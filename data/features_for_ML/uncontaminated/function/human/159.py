from transformers import AutoTokenizer as HFTokenizer

def from_pretrained(model_config):
        return HFTokenizer.from_pretrained(model_config.model_name, use_fast=True, legacy=False,
                                           local_files_only=model_config.local_only)