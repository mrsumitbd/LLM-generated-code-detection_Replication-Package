def merge(a, b):
    if a is MISSING:
        return b
    if b is MISSING:
        return a
    if isinstance(a, dict) and isinstance(b, dict):
        result = {**a}
        for key, value in b.items():
            result[key] = merge(result.get(key), value)
        return result
    if isinstance(a, list) and isinstance(b, list):
        result = a.copy()
        for index, value in enumerate(b):
            if index >= len(a):
                result[index] = value
            else:
                result[index] = merge(result[index], value)
        return result
    # Favor present values over missing ones
    if b is None:
        return a
    # Later values overwrite earier ones
    return b