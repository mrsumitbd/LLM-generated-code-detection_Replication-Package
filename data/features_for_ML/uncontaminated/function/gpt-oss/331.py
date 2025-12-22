def unexpect_error(context: str = None, error: Exception = None):
    """
    Raise an exception for an unexpected error, optionally adding context.

    Parameters
    ----------
    context : str, optional
        A string describing the context in which the error occurred.
    error : Exception, optional
        The original exception that was caught.

    Raises
    ------
    RuntimeError
        If no error is provided, or if a context is supplied and the error
        should be wrapped in a RuntimeError.
    Exception
        If an error is provided and no context is supplied, the original
        exception is re‑raised.
    """
    if error is None:
        # No error provided – raise a generic RuntimeError with context if any
        raise RuntimeError(f"Unexpected error: {context or 'No context'}")

    # An error was provided
    if context:
        # Wrap the original error in a RuntimeError to add context
        raise RuntimeError(f"{context}: {error}") from error
    else:
        # No context – re‑raise the original exception
        raise error