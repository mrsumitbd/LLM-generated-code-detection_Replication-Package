import re

def path_to_regex(path: str) -> str:
    """
    Converts a file path string to a regular expression pattern.
    
    Args:
        path (str): The file path to be converted.
        
    Returns:
        str: The regular expression pattern.
    """
    pattern = r'^'
    for i, char in enumerate(path):
        if char == '*':
            pattern += r'[^/]*'
        elif char == '?':
            pattern += r'[^/]'
        elif char == '/':
            pattern += r'\/'
        else:
            pattern += re.escape(char)
    pattern += r'$'
    return pattern