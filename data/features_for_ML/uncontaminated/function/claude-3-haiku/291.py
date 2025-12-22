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
    result = {}

    if use_reasoning:
        result["outputs"] = outputs
        result["reference_outputs"] = reference_outputs
        result["rubric"] = rubric
        result["exclude_keys"] = exclude_keys
        result["list_match_mode"] = list_match_mode

    return result