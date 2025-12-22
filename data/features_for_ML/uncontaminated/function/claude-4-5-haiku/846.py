def _get(
    d: Dict[str, Any], expected_type: Type[T], key: str, default: Optional[T] = None
) -> Optional[T]:
    """Get value from dictionary and verify expected type."""
    if key not in d:
        return default
    
    value = d[key]
    
    if value is None:
        return default
    
    if not isinstance(value, expected_type):
        raise TypeError(f"Expected {expected_type.__name__} for key '{key}', got {type(value).__name__}")
    
    return value