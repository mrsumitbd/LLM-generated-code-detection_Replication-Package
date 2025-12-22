def _get(
    d: Dict[str, Any], expected_type: Type[T], key: str, default: Optional[T] = None
) -> Optional[T]:
    value = d.get(key, default)
    if value is not None and not isinstance(value, expected_type):
        raise TypeError(f"Value for key '{key}' is not of expected type {expected_type.__name__}")
    return value