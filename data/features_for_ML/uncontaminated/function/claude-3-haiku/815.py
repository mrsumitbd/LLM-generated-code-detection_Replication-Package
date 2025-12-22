def sanitize_input(text: str) -> str:
    # Remove potentially dangerous characters
    sanitized_text = text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
    return sanitized_text