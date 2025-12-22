def is_gemma_model(model_name: str) -> bool:
    """
    Return True if the given model name corresponds to a Gemma model.

    Gemma models are typically named with a prefix or substring "gemma"
    (e.g., "gemma-2b", "gemma-7b", "gemma-2b-gguf", etc.). This function
    performs a case‑insensitive check for the presence of the substring
    "gemma" in the model name.

    Parameters
    ----------
    model_name : str
        The name of the model to check.

    Returns
    -------
    bool
        True if the model name indicates a Gemma model, False otherwise.
    """
    if not isinstance(model_name, str):
        return False
    return "gemma" in model_name.lower()