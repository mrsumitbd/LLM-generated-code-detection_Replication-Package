import re

def apply_assignment_spacing(line: str, use_spaces: bool = True) -> str:
    """
    Apply consistent spacing around assignment operators.

    Args:
        line: The line to format
        use_spaces: Whether to use spaces around operators

    Returns:
        The formatted line
    """
    # List of assignment operators (longest first to avoid partial matches)
    ops = [
        '>>=',
        '<<=',
        '**=',
        '//=',
        '+=',
        '-=',
        '*=',
        '/=',
        '%=',
        '&=',
        '|=',
        '^=',
        '=',
    ]

    # Build a regex pattern that matches any of the operators surrounded by optional whitespace
    # We use a non-capturing group for the operator list
    op_pattern = r'\s*(' + '|'.join(map(re.escape, ops)) + r')\s*'

    # Replacement string: either spaced or unspaced
    replacement = r' \1 ' if use_spaces else r'\1'

    # Perform the substitution
    formatted = re.sub(op_pattern, replacement, line)

    # If we added spaces, we might have introduced leading/trailing spaces; preserve original indentation
    # Strip only the added spaces around the operator, not the line indentation
    # The regex already preserves indentation, so we can return as is
    return formatted