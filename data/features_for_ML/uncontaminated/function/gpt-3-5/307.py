def validate_regex(value: str | None) -> str | None:
    import re
    if value is None:
        return None
    try:
        re.compile(value)
        return value
    except re.error:
        return None