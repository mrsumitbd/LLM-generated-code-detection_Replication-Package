from transformers import AutoTokenizer

def init_tokenizer(bert_model_path):
    """
    Load and return a Hugging Face tokenizer for the specified BERT model.

    Parameters
    ----------
    bert_model_path : str
        Path or identifier of the BERT model to load the tokenizer from.

    Returns
    -------
    tokenizer : transformers.PreTrainedTokenizer
        The tokenizer instance ready for use.
    """
    return AutoTokenizer.from_pretrained(bert_model_path)