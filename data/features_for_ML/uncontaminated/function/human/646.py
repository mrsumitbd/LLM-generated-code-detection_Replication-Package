from llama_index.core.llms.llm import LLM

def get_nothink_str(llm: LLM):
    if "glm-" in llm.metadata.model_name.lower():
        return "/nothink"
    return "/no_think"