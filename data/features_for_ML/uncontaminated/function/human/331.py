def unexpect_error(context: str = None, error: Exception = None):
    if context is None and error is None:
        message = "An unexpected error occurred."
    elif context and error:
        message = f"{context}: {type(error).__name__}: {str(error)}"
    elif error:
        message = f"An unexpected error occurred: {type(error).__name__}: {str(error)}"
    else:
        message = context

    return error(
        status_code=500,
        message=message,
        type="unknown_error",
        param=None,
        code=None,
    )