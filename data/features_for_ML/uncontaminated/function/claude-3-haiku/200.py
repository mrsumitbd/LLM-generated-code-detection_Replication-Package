def INPUT_TYPES(s):
    if isinstance(s, str):
        return "string"
    elif isinstance(s, int):
        return "integer"
    elif isinstance(s, float):
        return "float"
    elif isinstance(s, bool):
        return "boolean"
    elif isinstance(s, list):
        return "list"
    elif isinstance(s, tuple):
        return "tuple"
    elif isinstance(s, dict):
        return "dictionary"
    elif isinstance(s, set):
        return "set"
    else:
        return "unknown"