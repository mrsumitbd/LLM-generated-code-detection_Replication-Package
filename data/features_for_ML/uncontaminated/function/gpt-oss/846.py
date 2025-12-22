from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar("T")

def _get(
    d: Dict[str, Any], expected_type: Type[T], key: str, default: Optional[T] = None
) -> Optional[T]:
    """Get value from dictionary and verify expected type."""
    if key not in d:
        return default

    value = d[key]

    # Allow None as a valid value regardless of expected_type
    if value is None:
        return None

    if not isinstance(value, expected_type):
        raise TypeError(
            f"Expected value for key '{key}' to be of type {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )

    return value