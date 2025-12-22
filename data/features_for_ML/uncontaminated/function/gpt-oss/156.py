def _custom_policy(ctx, func, *args, **kwargs):
    """
    A simple custom policy that optionally skips the function call based on the
    context. The context can be a mapping or an object with a `skip` attribute.
    If `skip` is truthy, the function is not called and `None` is returned.
    Otherwise, the function is called with the supplied arguments and its
    result is returned unchanged.
    """
    # Determine whether to skip based on the context
    skip = False
    if isinstance(ctx, dict):
        skip = ctx.get("skip", False)
    else:
        skip = getattr(ctx, "skip", False)

    if skip:
        return None

    # Call the function and return its result
    return func(*args, **kwargs)