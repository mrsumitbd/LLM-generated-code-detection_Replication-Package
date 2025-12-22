def sanitize_input(text: str) -> str:
    import re
    return re.sub(r'[^\w\s]', '', text)