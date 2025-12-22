import re

def sanitize_input(text: str) -> str:
    """
    Remove potentially dangerous characters from the input string.
    This function strips characters that are commonly used in injection
    attacks or can break HTML/SQL contexts.
    """
    # Define a pattern for characters to remove
    # Commonly dangerous: < > & ' " / \ ` ; : = ( ) { } [ ] | ^ ~
    dangerous_chars = r"[<>&'\"/\\`;\:\=\(\)\{\}\[\]\|\^~]"
    # Replace them with an empty string
    sanitized = re.sub(dangerous_chars, "", text)
    # Optionally strip leading/trailing whitespace
    return sanitized.strip()