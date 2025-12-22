from typing import Literal, Optional, Dict, Any, Union
from openevals.llm import (
    _create_llm_as_judge_scorer,
    _create_async_llm_as_judge_scorer,
    ModelClient,
)
from langchain_core.language_models.chat_models import BaseChatModel

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
    if not judge and not model and len(rubric) != 0:
        raise ValueError("When passing rubric, either judge or model must be provided")
    if len(rubric) == 0 and (judge or model):
        raise ValueError(
            "A judge model is only used and may only be provided when also passing a rubric for grading specific keys."
        )