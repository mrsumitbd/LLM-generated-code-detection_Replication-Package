def _prepare_parameters(
    *,
    outputs: Any,
    reference_outputs: Any,
    rubric: Dict[str, str],
    exclude_keys: list[str],
    use_reasoning: bool,
    list_match_mode: Literal[
        "superset", "subset", "same_elements", "ordered"
    ] = "same_elements",
):
    """Prepare and validate parameters for evaluation."""
    
    # Validate list_match_mode
    valid_modes = {"superset", "subset", "same_elements", "ordered"}
    if list_match_mode not in valid_modes:
        raise ValueError(
            f"list_match_mode must be one of {valid_modes}, got {list_match_mode}"
        )
    
    # Validate rubric is a dictionary
    if not isinstance(rubric, dict):
        raise TypeError(f"rubric must be a dictionary, got {type(rubric)}")
    
    # Validate rubric values are strings
    for key, value in rubric.items():
        if not isinstance(value, str):
            raise TypeError(
                f"rubric values must be strings, got {type(value)} for key {key}"
            )
    
    # Validate exclude_keys is a list
    if not isinstance(exclude_keys, list):
        raise TypeError(f"exclude_keys must be a list, got {type(exclude_keys)}")
    
    # Validate exclude_keys contains strings
    for key in exclude_keys:
        if not isinstance(key, str):
            raise TypeError(
                f"exclude_keys must contain strings, got {type(key)}"
            )
    
    # Validate use_reasoning is a boolean
    if not isinstance(use_reasoning, bool):
        raise TypeError(f"use_reasoning must be a boolean, got {type(use_reasoning)}")
    
    # Validate outputs and reference_outputs are not None
    if outputs is None:
        raise ValueError("outputs cannot be None")
    if reference_outputs is None:
        raise ValueError("reference_outputs cannot be None")
    
    return {
        "outputs": outputs,
        "reference_outputs": reference_outputs,
        "rubric": rubric,
        "exclude_keys": exclude_keys,
        "use_reasoning": use_reasoning,
        "list_match_mode": list_match_mode,
    }