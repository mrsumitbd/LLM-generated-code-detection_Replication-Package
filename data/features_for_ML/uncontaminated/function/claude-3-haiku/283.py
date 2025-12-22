def diamond_peptidase_options(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return result.upper()
        elif isinstance(result, list):
            return [item.upper() for item in result]
        elif isinstance(result, dict):
            return {key: value.upper() for key, value in result.items()}
        else:
            return result
    return wrapper