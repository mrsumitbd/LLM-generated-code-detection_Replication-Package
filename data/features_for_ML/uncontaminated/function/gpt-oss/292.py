import os
import torch
from typing import Any

# Importing transformers lazily to avoid heavy imports when not needed
def _get_transformers():
    from transformers import AutoModel, AutoTokenizer, AutoConfig
    return AutoModel, AutoTokenizer, AutoConfig

def save_pretrained(args: Any) -> None:
    """
    Load a checkpoint from `args.ckpt_path`, instantiate a model (and optionally a tokenizer),
    and save them to `args.output_dir` using the HuggingFace `save_pretrained` API.

    Expected attributes on `args`:
        - ckpt_path: Path to the checkpoint file (torch checkpoint or state_dict).
        - output_dir: Directory where the model and tokenizer will be saved.
        - model_name_or_path: Name or path of the base model to use for configuration.
        - tokenizer_name_or_path (optional): Name or path of the tokenizer to use.
        - config_path (optional): Path to a config file to load instead of the base model.
        - model_class (optional): A subclass of `transformers.PreTrainedModel` to instantiate.
    """
    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Load the checkpoint
    ckpt = torch.load(args.ckpt_path, map_location="cpu")

    # Import transformers components
    AutoModel, AutoTokenizer, AutoConfig = _get_transformers()

    # Load configuration
    if hasattr(args, "config_path") and args.config_path:
        config = AutoConfig.from_pretrained(args.config_path)
    else:
        config = AutoConfig.from_pretrained(args.model_name_or_path)

    # Instantiate the model
    if hasattr(args, "model_class") and args.model_class:
        # If a custom model class is provided, use it
        model = args.model_class.from_pretrained(
            args.model_name_or_path,
            config=config,
            state_dict=ckpt,
        )
    else:
        # Default to AutoModel
        model = AutoModel.from_pretrained(
            args.model_name_or_path,
            config=config,
            state_dict=ckpt,
        )

    # Save the model
    model.save_pretrained(args.output_dir)

    # Instantiate and save the tokenizer if requested
    tokenizer_name = getattr(args, "tokenizer_name_or_path", None)
    if tokenizer_name:
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    else:
        tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path)

    tokenizer.save_pretrained(args.output_dir)