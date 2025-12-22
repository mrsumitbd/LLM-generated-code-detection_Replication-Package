def wrapper(*args, **kwargs):  # type: ignore
    """
    A wrapper function that can handle both positional and keyword arguments.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        The result of the wrapped function.
    """
    def inner_wrapper(func):
        def wrapped_function(*inner_args, **inner_kwargs):
            return func(*inner_args, **inner_kwargs)
        return wrapped_function
    return inner_wrapper