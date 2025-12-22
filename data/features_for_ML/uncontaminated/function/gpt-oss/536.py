import torch
from typing import List, Optional, Dict, Any

def prepare(
    model_spec,
    system_message,
    tokenizer,
    pixel_values,
    question,
    history: Optional[List[tuple]] = None,
    num_patches_list: Optional[List[int]] = None,
    IMG_START_TOKEN: str = '<img>',
    IMG_END_TOKEN: str = '</img>',
    IMG_CONTEXT_TOKEN: str = '<IMG_CONTEXT>',
    llm_only: bool = False,
) -> Dict[str, Any]:
    """
    Prepare inputs for a multimodal LLM.

    Parameters
    ----------
    model_spec : Any
        Unused in this implementation but kept for API compatibility.
    system_message : str
        System prompt to prepend.
    tokenizer : transformers.PreTrainedTokenizer
        Tokenizer with special tokens for image context.
    pixel_values : torch.Tensor or None
        Image features to be passed to the model.
    question : str
        Current user question.
    history : list of (str, str) or None
        Conversation history as list of (question, answer) tuples.
    num_patches_list : list of int or None
        Number of image patches per image. If None, defaults to 1.
    IMG_START_TOKEN : str
        Token marking the start of an image region.
    IMG_END_TOKEN : str
        Token marking the end of an image region.
    IMG_CONTEXT_TOKEN : str
        Token representing a single image patch.
    llm_only : bool
        If True, ignore image tokens and pixel values.

    Returns
    -------
    dict
        Dictionary containing `input_ids`, `pixel_values`, and `attention_mask`.
    """
    # Helper to encode a string with the tokenizer
    def _enc(text: str) -> List[int]:
        return tokenizer.encode(text, add_special_tokens=False)

    # Build the prompt
    prompt_tokens = []

    # System message
    if system_message:
        prompt_tokens += _enc(system_message)

    # History
    if history:
        for hist_q, hist_a in history:
            # User turn
            prompt_tokens += _enc("User: ")
            prompt_tokens += _enc(hist_q)
            prompt_tokens += [tokenizer.eos_token_id]
            # Assistant turn
            prompt_tokens += _enc("Assistant: ")
            prompt_tokens += _enc(hist_a)
            prompt_tokens += [tokenizer.eos_token_id]

    # Current question with image tokens if applicable
    prompt_tokens += _enc("User: ")
    if not llm_only and pixel_values is not None:
        # Insert image start token
        prompt_tokens += _enc(IMG_START_TOKEN)
        # Insert image context tokens
        num_patches = 1
        if num_patches_list:
            num_patches = num_patches_list[0]
        img_ctx_id = tokenizer.convert_tokens_to_ids(IMG_CONTEXT_TOKEN)
        prompt_tokens += [img_ctx_id] * num_patches
        # Insert image end token
        prompt_tokens += _enc(IMG_END_TOKEN)

    # Add the question text
    prompt_tokens += _enc(question)
    prompt_tokens += [tokenizer.eos_token_id]

    # Assistant placeholder
    prompt_tokens += _enc("Assistant: ")

    # Convert to tensor
    input_ids = torch.tensor(prompt_tokens, dtype=torch.long)

    # Attention mask (all ones, no padding)
    attention_mask = torch.ones_like(input_ids, dtype=torch.long)

    # Build output dict
    out = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
    }

    # Include pixel values if provided and not llm_only
    if pixel_values is not None and not llm_only:
        out["pixel_values"] = pixel_values

    return out