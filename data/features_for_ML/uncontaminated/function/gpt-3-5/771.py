def validate_regex(pattern):
    import re
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False