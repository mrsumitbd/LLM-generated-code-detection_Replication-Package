from langchain.chat_models import ChatOpenAI
from langchain.schema import FunctionCallingLLM

def get_local_llm(
    name: str,
    temperature: float | None = None,
    top_p: float | None = None,
) -> FunctionCallingLLM:
    """
    Return a local LLM instance that supports function calling.

    Parameters
    ----------
    name : str
        The name or identifier of the local model to load.
    temperature : float | None, optional
        Sampling temperature. If None, the default value of the model is used.
    top_p : float | None, optional
        Top-p (nucleus) sampling. If None, the default value of the model is used.

    Returns
    -------
    FunctionCallingLLM
        An LLM instance that implements the FunctionCallingLLM protocol.
    """
    # Build keyword arguments for the model
    model_kwargs: dict[str, object] = {}
    if temperature is not None:
        model_kwargs["temperature"] = temperature
    if top_p is not None:
        model_kwargs["top_p"] = top_p

    # Instantiate the local LLM
    return ChatOpenAI(model_name=name, **model_kwargs)