from __future__ import annotations

from typing import Any, Dict, Literal, List

def _prepare_parameters(
    *,
    outputs: Any,
    reference_outputs: Any,
    rubric: Dict[str, str],
    exclude_keys: List[str],
    use_reasoning: bool,
    list_match_mode: Literal[
        "superset", "subset", "same_elements", "ordered"
    ] = "same_elements",
):
    """
    Prepare and sanitize parameters for evaluation.

    Parameters
    ----------
    outputs : Any
        The model's output. Can be a dict, list, or scalar.
    reference_outputs : Any
        The expected output. Can be a dict, list, or scalar.
    rubric : Dict[str, str]
        A mapping of evaluation criteria to descriptions.
    exclude_keys : List[str]
        Keys to remove from any dict structures in ``outputs`` or
        ``reference_outputs``.
    use_reasoning : bool
        If ``True``, ensure that a ``reasoning`` key exists in the
        output dictionaries (set to ``None`` if missing).
    list_match_mode : Literal["superset", "subset", "same_elements", "ordered"]
        The mode used to compare list outputs.  This value is passed
        unchanged to the caller.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the cleaned ``outputs`` and
        ``reference_outputs`` along with the original ``rubric``,
        ``use_reasoning`` flag and ``list_match_mode``.
    """
    # Validate list_match_mode
    valid_modes = {"superset", "subset", "same_elements", "ordered"}
    if list_match_mode not in valid_modes:
        raise ValueError(
            f"Invalid list_match_mode: {list_match_mode!r}. "
            f"Expected one of {sorted(valid_modes)}."
        )

    def _filter(obj: Any) -> Any:
        """
        Recursively remove keys listed in ``exclude_keys`` from dicts.
        """
        if isinstance(obj, dict):
            return {
                k: _filter(v)
                for k, v in obj.items()
                if k not in exclude_keys
            }
        if isinstance(obj, list):
            return [_filter(v) for v in obj]
        return obj

    cleaned_outputs = _filter(outputs)
    cleaned_reference = _filter(reference_outputs)

    # Ensure reasoning key if requested
    if use_reasoning:

        def _ensure_reasoning(o: Any) -> Any:
            if isinstance(o, dict):
                if "reasoning" not in o:
                    o["reasoning"] = None
                # Recurse into nested structures
                for k, v in o.items():
                    o[k] = _ensure_reasoning(v)
            elif isinstance(o, list):
                return [_ensure_reasoning(v) for v in o]
            return o

        cleaned_outputs = _ensure_reasoning(cleaned_outputs)
        cleaned_reference = _ensure_reasoning(cleaned_reference)

    return {
        "outputs": cleaned_outputs,
        "reference_outputs": cleaned_reference,
        "rubric": rubric,
        "use_reasoning": use_reasoning,
        "list_match_mode": list_match_mode,
    }