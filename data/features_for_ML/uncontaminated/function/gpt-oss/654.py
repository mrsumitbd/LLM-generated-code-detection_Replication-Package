from typing import Dict, Optional, Union

def _validate_parameters(
    *,
    judge: Optional[Union["ModelClient", "BaseChatModel"]],
    model: Optional[str],
    rubric: Dict[str, str],
) -> None:
    """
    Validate that judge/model and rubric parameters are consistent.

    Args:
        judge: The judge model client
        model: The model name string
        rubric: The rubric dictionary

    Raises:
        ValueError: If the combination of parameters is invalid
    """
    # 1. Validate that rubric is a non‑empty dict of str → str
    if not isinstance(rubric, dict):
        raise ValueError(f"rubric must be a dict, got {type(rubric).__name__}")
    if not rubric:
        raise ValueError("rubric must contain at least one key/value pair")
    for k, v in rubric.items():
        if not isinstance(k, str):
            raise ValueError(f"rubric key {k!r} is not a string")
        if not isinstance(v, str):
            raise ValueError(f"rubric value for key {k!r} is not a string")

    # 2. Validate judge type
    if judge is not None:
        # Import lazily to avoid circular imports
        try:
            from langchain_core.language_models import BaseChatModel
        except Exception:
            BaseChatModel = None  # type: ignore
        try:
            from langchain_openai import OpenAI
        except Exception:
            OpenAI = None  # type: ignore

        # We accept any object that has a `client` attribute or is a BaseChatModel
        if not (
            hasattr(judge, "client")
            or (BaseChatModel is not None and isinstance(judge, BaseChatModel))
        ):
            raise ValueError(
                f"judge must be a ModelClient or BaseChatModel instance, got {type(judge).__name__}"
            )

    # 3. Validate model type
    if model is not None and not isinstance(model, str):
        raise ValueError(f"model must be a string, got {type(model).__name__}")

    # 4. Ensure that exactly one of judge or model is provided
    if judge is None and model is None:
        raise ValueError("either judge or model must be provided")
    if judge is not None and model is not None:
        raise ValueError("cannot provide both judge and model; choose one")