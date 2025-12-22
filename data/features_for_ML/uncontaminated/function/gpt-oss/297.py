from typing import Any, Dict

def make_forwardref(annotation: str, globalns: Dict[str, Any]) -> Any:
    """
    Evaluate a forward reference string using the provided global namespace.

    Parameters
    ----------
    annotation : str
        The forward reference string to evaluate.
    globalns : Dict[str, Any]
        The global namespace to use for evaluation.

    Returns
    -------
    Any
        The evaluated type if successful; otherwise, the original string.
    """
    try:
        # Attempt to evaluate the annotation string in the given namespace.
        return eval(annotation, globalns)
    except Exception:
        # If evaluation fails, return the original string unchanged.
        return annotation