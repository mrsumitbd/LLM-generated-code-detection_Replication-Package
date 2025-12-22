from typing import FunctionCallingLLM

def get_local_llm(
    name: str,
    temperature: float | None = None,
    top_p: float | None = None,
) -> FunctionCallingLLM:
    from langchain.llms.openai import OpenAI
    from langchain.llms.base import FunctionCallingLLM

    llm = OpenAI(
        model_name=name,
        temperature=temperature,
        top_p=top_p,
    )

    return FunctionCallingLLM(llm)