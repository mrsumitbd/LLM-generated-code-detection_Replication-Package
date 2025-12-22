def _str_to_int(x: str) -> bool:
    """
    Return True if the string `x` represents a valid integer, otherwise False.
    Leading/trailing whitespace is allowed, as is an optional leading '+' or '-'.
    """
    if not isinstance(x, str):
        return False
    s = x.strip()
    if not s:
        return False
    # Optional sign
    if s[0] in '+-':
        s = s[1:]
    # After removing sign, must have at least one digit
    if not s:
        return False
    # All remaining characters must be digits
    return s.isdigit()