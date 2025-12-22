from transformers import AutoConfig

def is_gemma_model(model_name: str) -> bool:
    hf_config = AutoConfig.from_pretrained(model_name, trust_remote_code=True)
    return hasattr(hf_config, "model_type") and hf_config.model_type in [
        "gemma2",
        "gemma3",
        "gemma3_text",
    ]