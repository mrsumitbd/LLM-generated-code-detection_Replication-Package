def get_local_llm(name: str, temperature: float = None, top_p: float = None) -> FunctionCallingLLM:
    return FunctionCallingLLM(name, temperature, top_p)