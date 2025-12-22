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
    return {
        "outputs": outputs,
        "reference_outputs": reference_outputs,
        "rubric": rubric,
        "exclude_keys": exclude_keys,
        "use_reasoning": use_reasoning,
        "list_match_mode": list_match_mode
    }