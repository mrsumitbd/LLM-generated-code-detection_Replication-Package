import torch
from transformers import AutoModel, AutoTokenizer

def from_pretrained(model_config):
    """
    Load a pretrained model (and optionally a tokenizer) based on a configuration dictionary.

    Parameters
    ----------
    model_config : dict
        Configuration dictionary that may contain the following keys:
        - "model_name" (str): Name of a Hugging Face model to load via AutoModel.
        - "pretrained_path" (str): Path to a local checkpoint file to load via torch.load.
        - "tokenizer_name" (str, optional): Name of a tokenizer to load via AutoTokenizer.
        - "device" (str, optional): Target device for the model (default: "cpu").

    Returns
    -------
    tuple
        A tuple `(model, tokenizer)` where `model` is a PyTorch model and `tokenizer`
        is either a Hugging Face tokenizer or `None` if not requested.
    """
    if not isinstance(model_config, dict):
        raise ValueError("model_config must be a dictionary")

    model_name = model_config.get("model_name")
    pretrained_path = model_config.get("pretrained_path")
    device = model_config.get("device", "cpu")

    # Load the model
    if pretrained_path:
        # Load a local checkpoint
        model = torch.load(pretrained_path, map_location=device)
    elif model_name:
        # Load from Hugging Face hub
        model = AutoModel.from_pretrained(model_name)
    else:
        raise ValueError("Either 'model_name' or 'pretrained_path' must be provided in model_config")

    # Move model to the requested device
    model.to(device)

    # Load tokenizer if requested
    tokenizer = None
    tokenizer_name = model_config.get("tokenizer_name")
    if tokenizer_name:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    return model, tokenizer