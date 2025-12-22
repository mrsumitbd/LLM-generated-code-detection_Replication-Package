def sanitize_input(text: str) -> str:
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '|', '`', '$', '(', ')', '{', '}', '[', ']', '\\', '\n', '\r', '\0']
    result = text
    for char in dangerous_chars:
        result = result.replace(char, '')
    return result