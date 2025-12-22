def get_nothink_str(llm: LLM):
    return llm.model_name if hasattr(llm, 'model_name') else str(llm)