def validate_regex(pattern):
    """
    Validate that a regex pattern is valid.
    
    Args:
        pattern: The regex pattern to validate
        
    Returns:
        True if valid, False if invalid
    """
    import re
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False