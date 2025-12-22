def get_local_llm(
    name: str,
    temperature: float | None = None,
    top_p: float | None = None,
) -> FunctionCallingLLM:
    from llama_index.llms.ollama import Ollama
    
    kwargs = {
        "model": name,
        "request_timeout": 120.0,
    }
    
    if temperature is not None:
        kwargs["temperature"] = temperature
    
    if top_p is not None:
        kwargs["top_p"] = top_p
    
    return Ollama(**kwargs)