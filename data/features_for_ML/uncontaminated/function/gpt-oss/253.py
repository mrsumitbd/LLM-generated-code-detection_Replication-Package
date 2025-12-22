from __future__ import annotations

from typing import Any, Dict

# Import the MessageRecipient class from the appropriate module.
# Adjust the import path if the class lives elsewhere.
try:
    from .models import MessageRecipient  # type: ignore
except Exception:  # pragma: no cover
    # Fallback for environments where the relative import fails.
    from models import MessageRecipient  # type: ignore


def _camel_case(name: str) -> str:
    """Convert snake_case to CamelCase."""
    return ''.join(part.capitalize() for part in name.split('_'))


def from_json(data: Dict[str, Any]) -> "MessageRecipient":
    """
    Create a :class:`MessageRecipient` instance from a JSON dictionary.

    The function accepts a dictionary that may contain keys in either
    snake_case or CamelCase.  If the dictionary contains a top‑level
    ``recipient`` key whose value is a dictionary, that nested dictionary
    is used as the source of fields.

    Parameters
    ----------
    data:
        The JSON dictionary to convert.

    Returns
    -------
    MessageRecipient
        An instance populated with the data from the dictionary.

    Raises
    ------
    TypeError
        If ``data`` is not a dictionary.
    ValueError
        If required fields for :class:`MessageRecipient` are missing.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")

    # If the payload is wrapped in a ``recipient`` key, use that.
    if "recipient" in data and isinstance(data["recipient"], dict):
        data = data["recipient"]

    # Build keyword arguments for the MessageRecipient constructor.
    kwargs: Dict[str, Any] = {}
    annotations = getattr(MessageRecipient, "__annotations__", {})
    for field in annotations:
        if field in data:
            kwargs[field] = data[field]
        else:
            # Try CamelCase variant.
            camel = _camel_case(field)
            if camel in data:
                kwargs[field] = data[camel]

    # Instantiate the MessageRecipient.
    return MessageRecipient(**kwargs)