def categorize_error(exception: Exception) -> Tuple[ErrorCategory, str]:
    if isinstance(exception, ValueError):
        return ErrorCategory.INPUT_ERROR, "Check the input value and try again."
    elif isinstance(exception, KeyError):
        return ErrorCategory.KEY_ERROR, "The specified key does not exist."
    elif isinstance(exception, FileNotFoundError):
        return ErrorCategory.FILE_ERROR, "The specified file was not found."
    else:
        return ErrorCategory.UNKNOWN_ERROR, "An unknown error occurred. Please try again later."