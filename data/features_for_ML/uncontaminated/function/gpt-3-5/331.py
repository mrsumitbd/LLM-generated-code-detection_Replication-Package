def unexpect_error(context: str = None, error: Exception = None):
    if context is not None:
        print(f"Unexpected error occurred in context: {context}")
    if error is not None:
        print(f"Error details: {error}")