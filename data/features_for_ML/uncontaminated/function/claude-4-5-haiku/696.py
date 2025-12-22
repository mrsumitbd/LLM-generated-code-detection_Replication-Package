import re

def is_valid_url(url):
    """
    Validate if a given string is a valid URL.
    
    Args:
        url: A string to validate as a URL
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    # URL regex pattern that matches common URL formats
    url_pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
    
    if not isinstance(url, str):
        return False
    
    if not url or len(url) > 2048:
        return False
    
    if re.match(url_pattern, url):
        return True
    
    return False