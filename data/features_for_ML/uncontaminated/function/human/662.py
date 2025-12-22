from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.llms.openai_like import OpenAILike
from syftr.configuration import (
    NON_OPENAI_CONTEXT_WINDOW_FACTOR,
    AnthropicVertexLLM,
    AzureAICompletionsLLM,
    AzureOpenAILLM,
    CerebrasLLM,
    OpenAILikeLLM,
    OpenAIResponsesLLM,
    Settings,
    VertexAILLM,
    cfg,
)

def get_local_llm(
    name: str,
    temperature: float | None = None,
    top_p: float | None = None,
) -> FunctionCallingLLM:
    assert name in LLM_NAMES__LOCAL_MODELS, (
        f"LLM '{name}' not found in configured local models. "
        f"Available local models: {LLM_NAMES__LOCAL_MODELS}"
    )
    model = next(
        model for model in cfg.local_models.generative or [] if model.model_name == name
    )
    if top_p is not None:
        model.additional_kwargs["top_p"] = top_p
    return OpenAILike(  # type: ignore
        api_base=str(model.api_base),
        api_key=model.api_key.get_secret_value()
        if model.api_key is not None
        else cfg.local_models.default_api_key.get_secret_value(),
        model=model.model_name,
        temperature=temperature if temperature is not None else model.temperature,
        max_tokens=model.max_tokens,
        context_window=_scale(model.context_window),
        is_chat_model=model.is_chat_model,
        is_function_calling_model=model.is_function_calling_model,
        timeout=model.timeout,
        max_retries=model.max_retries,
        additional_kwargs=model.additional_kwargs,
    )