def _validate_parameters(
    *,
    judge: Optional[Union[ModelClient, BaseChatModel]],
    model: Optional[str],
    rubric: Dict[str, str],
) -> None:
    if judge is None and model is None:
        raise ValueError("Both judge and model cannot be None")
    if judge is not None and model is not None:
        raise ValueError("Both judge and model cannot be provided at the same time")
    if not rubric:
        raise ValueError("Rubric cannot be empty")