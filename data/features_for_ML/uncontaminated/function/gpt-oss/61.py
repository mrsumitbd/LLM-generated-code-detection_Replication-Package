import ast

def INPUT_TYPES(s):
    """
    Determine the Python type represented by the string `s`.

    The function attempts to safely evaluate the string using
    `ast.literal_eval`. If evaluation succeeds, the name of the
    resulting type is returned. If evaluation fails (e.g. the
    string is not a valid Python literal), the function assumes
    the input is a plain string and returns 'str'.
    """
    try:
        value = ast.literal_eval(s)
        return type(value).__name__
    except Exception:
        return "str"