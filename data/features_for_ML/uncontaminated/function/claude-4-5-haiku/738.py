def is_gemma_model(model_name: str) -> bool:
    """Check if a model name is a Gemma model."""
    gemma_models = [
        "gemma-7b",
        "gemma-7b-it",
        "gemma-2b",
        "gemma-2b-it",
        "gemma2-9b",
        "gemma2-27b",
        "gemma-1.1-7b-it",
        "gemma-1.1-2b-it",
    ]
    
    model_name_lower = model_name.lower()
    
    for gemma_model in gemma_models:
        if gemma_model in model_name_lower:
            return True
    
    return False