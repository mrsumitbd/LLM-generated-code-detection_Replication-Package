def _get(
    d: Dict[str, Any], expected_type: Type[T], key: str, default: Optional[T] = None
) -> Optional[T]:
    """Get value from dictionary and verify expected type."""
    try:
        value = d.get(key, default)
        if value is None or isinstance(value, expected_type):
            return value
        else:
            raise TypeError(f"Value for key '{key}' is not of expected type {expected_type}")
    except (KeyError, TypeError) as e:
        return default