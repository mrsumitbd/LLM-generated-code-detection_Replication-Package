import torch
from typing import Sequence
from transformers import GenerationMixin, PreTrainedTokenizer


def __rollout(
    model: GenerationMixin,
    tokenizer: PreTrainedTokenizer,
    prompt: Sequence[str],
    device: str = "cpu",
) -> Sequence[str]:
    """
    Generate continuations for a sequence of prompts using the provided model and tokenizer.

    Parameters
    ----------
    model : GenerationMixin
        The model used for generation. It will be moved to the specified device.
    tokenizer : PreTrainedTokenizer
        Tokenizer used to encode the prompts and decode the generated tokens.
    prompt : Sequence[str]
        A sequence of prompt strings to generate continuations for.
    device : str, optional
        The device on which to run the model (e.g., "cpu" or "cuda").

    Returns
    -------
    Sequence[str]
        A list of generated strings, one for each prompt.
    """
    # Ensure the model is on the correct device
    model.to(device)

    # Prepare the output list
    outputs = []

    # Disable gradient calculations for inference
    with torch.no_grad():
        for text in prompt:
            # Encode the prompt
            input_ids = tokenizer.encode(text, return_tensors="pt").to(device)

            # Generate continuation
            # We use a reasonable default for max_new_tokens; this can be adjusted as needed.
            generated_ids = model.generate(
                input_ids,
                max_new_tokens=50,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id,
            )

            # Decode the generated tokens, skipping the prompt part
            # The generated_ids includes the input_ids; we want only the new tokens
            new_tokens = generated_ids[0, input_ids.shape[1] :]
            generated_text = tokenizer.decode(new_tokens, skip_special_tokens=True)

            outputs.append(generated_text)

    return outputs