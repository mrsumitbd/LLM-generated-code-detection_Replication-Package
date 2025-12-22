def wrapper(*args, **kwargs):  # noqa: ANN202
    """
    A wrapper function that can handle both positional and keyword arguments.

    Args:
        *args: Positional arguments passed to the function.
        **kwargs: Keyword arguments passed to the function.

    Returns:
        The result of the function call.
    """
    def inner_function(*inner_args, **inner_kwargs):
        """
        An inner function that can be used to call the original function.

        Args:
            *inner_args: Positional arguments to be passed to the original function.
            **inner_kwargs: Keyword arguments to be passed to the original function.

        Returns:
            The result of the original function call.
        """
        return original_function(*inner_args, **inner_kwargs)

    original_function = args[0]
    return inner_function