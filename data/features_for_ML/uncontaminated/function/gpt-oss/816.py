import inspect

def function_signature(self) -> str:
    """
    Returns the function signature as a string.

    Gets the string representation of the function's signature, including name, parameters, and return type.

    Args:
        None

    Returns:
        str: A string containing the complete function signature including the function name,
            parameters (if any), return type annotation (if present), and a colon.
    """
    # Get the bound method object for this function
    method = self.function_signature
    # Build the signature string
    sig_str = f"{method.__name__}{inspect.signature(method)}:"
    return sig_str