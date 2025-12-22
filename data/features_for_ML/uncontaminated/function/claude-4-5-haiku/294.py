def policy_fn(ctx, func, *args, **kwargs):
    """
    Execute a function with a given context, passing through args and kwargs.
    """
    return func(ctx, *args, **kwargs)