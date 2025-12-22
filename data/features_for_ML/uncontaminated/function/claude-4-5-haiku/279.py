def _is_true(valid) -> bool:
    if isinstance(valid, bool):
        return valid
    if isinstance(valid, str):
        return valid.lower() in ('true', '1', 'yes', 'on')
    if isinstance(valid, (int, float)):
        return valid != 0
    if valid is None:
        return False
    return bool(valid)