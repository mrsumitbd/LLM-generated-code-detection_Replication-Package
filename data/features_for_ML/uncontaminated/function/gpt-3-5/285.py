def _str_to_int(x: str) -> bool:
    try:
        int(x)
        return True
    except ValueError:
        return False