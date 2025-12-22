def is_gemma_model(model_name: str) -> bool:
    gemma_models = ["Gemma 1", "Gemma 2", "Gemma 3", "Gemma 4", "Gemma 5"]
    return model_name in gemma_models