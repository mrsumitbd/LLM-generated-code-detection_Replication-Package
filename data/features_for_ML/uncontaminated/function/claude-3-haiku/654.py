from typing import Optional, Union
from .model_client import ModelClient
from .base_chat_model import BaseChatModel

def _validate_parameters(
    *,
    judge: Optional[Union[ModelClient, BaseChatModel]],
    model: Optional[str],
    rubric: Dict[str, str],
) -> None:
    """Validate that judge/model and rubric parameters are consistent.

    Args:
        judge: The judge model client
        model: The model name string
        rubric: The rubric dictionary

    Raises:
        ValueError: If the combination of parameters is invalid
    """
    if judge is None and model is None:
        raise ValueError("Either judge or model must be provided.")
    if judge is not None and model is not None:
        raise ValueError("Only one of judge or model can be provided.")
    if not rubric:
        raise ValueError("Rubric must not be empty.")