def unexpect_error(context: str = None, error: Exception = None):
    """
    Raise an unexpected error with optional context and error information.
    """
    message = "An unexpected error occurred"
    
    if context:
        message += f" in {context}"
    
    if error:
        message += f": {type(error).__name__}: {str(error)}"
    
    raise RuntimeError(message)