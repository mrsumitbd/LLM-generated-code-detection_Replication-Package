def path_to_regex(path: str) -> str:
    import re
    path = re.sub(r'{\w+}', r'(\w+)', path)
    return f'^{path}$'