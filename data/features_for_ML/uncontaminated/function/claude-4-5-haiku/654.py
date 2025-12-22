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
    # Check that at least one of judge or model is provided
    if judge is None and model is None:
        raise ValueError(
            "Either 'judge' or 'model' must be provided. "
            "Cannot create a judge without specifying a model."
        )
    
    # Check that both judge and model are not provided simultaneously
    if judge is not None and model is not None:
        raise ValueError(
            "Cannot specify both 'judge' and 'model'. "
            "Provide either a judge instance or a model name, not both."
        )
    
    # Check that rubric is not empty
    if not rubric:
        raise ValueError(
            "The 'rubric' dictionary cannot be empty. "
            "Provide at least one criterion with its description."
        )
    
    # Check that all rubric values are non-empty strings
    for key, value in rubric.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"All rubric values must be non-empty strings. "
                f"Invalid value for key '{key}': {value!r}"
            )