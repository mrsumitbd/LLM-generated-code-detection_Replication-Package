import re

def validate_regex(value: str | None) -> str | None:
    """
    Validate that the given string is a valid regular expression.

    Parameters
    ----------
    value : str | None
        The regex pattern to validate. If None, the function returns None.

    Returns
    -------
    str | None
        The original pattern if it is a valid regex, otherwise None.

    Raises
    ------
    ValueError
        If the pattern is not a valid regular expression.
    """
    if value is None:
        return None

    try:
        re.compile(value)
    except re.error as exc:
        raise ValueError(f"Invalid regex pattern: {value!r}") from exc

    return value