def function_signature(self) -> str:
    """Returns the function signature as a string.

    Gets the string representation of the function's signature, including name, parameters, and return type.

    Args:
        None

    Returns:
        str: A string containing the complete function signature including the function name,
            parameters (if any), return type annotation (if present), and a colon.
    """
    import inspect
    
    sig = inspect.signature(self.__call__)
    params = str(sig)
    
    # Get return annotation if it exists
    return_annotation = sig.return_annotation
    if return_annotation != inspect.Signature.empty:
        return_str = f" -> {return_annotation.__name__}" if hasattr(return_annotation, '__name__') else f" -> {return_annotation}"
    else:
        return_str = ""
    
    # Get the function name
    func_name = self.__class__.__name__ if hasattr(self, '__class__') else 'function'
    
    return f"{func_name}{params}{return_str}:"