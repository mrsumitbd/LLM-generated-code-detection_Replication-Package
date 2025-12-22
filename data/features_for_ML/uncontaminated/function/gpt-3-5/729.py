def validate_pattern_for_direct_mode(ctx, param, value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{param} must be a string")
    if not value.startswith("direct:"):
        raise ValueError(f"{param} must start with 'direct:'")
    return value