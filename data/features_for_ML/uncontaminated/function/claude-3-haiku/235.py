def validate_expression(expression: str, allowed_keys: list[str]) -> None:
    allowed_keys_set = set(allowed_keys)
    for char in expression:
        if char not in allowed_keys_set:
            raise ValueError(f"Invalid character '{char}' in the expression.")