def policy_fn(ctx, func, *args, **kwargs):
    """
    Apply a policy to a function call.

    The policy can be provided in several ways:
    1. `ctx` itself is a callable that accepts a function and returns a wrapped function.
    2. `ctx` has a callable attribute `policy` that accepts the function and its arguments.
    3. `ctx` is a mapping (e.g., dict) containing a callable under the key `'policy'`.

    If none of the above apply, the function is called directly.
    """
    # 1. ctx is a callable that returns a wrapped function
    if callable(ctx):
        try:
            wrapped = ctx(func)
            if callable(wrapped):
                return wrapped(*args, **kwargs)
        except Exception:
            # If ctx is not a policy wrapper, fall back to other checks
            pass

    # 2. ctx has a callable attribute `policy`
    if hasattr(ctx, "policy") and callable(getattr(ctx, "policy")):
        return ctx.policy(func, *args, **kwargs)

    # 3. ctx is a mapping with a callable under 'policy'
    if isinstance(ctx, dict) and "policy" in ctx and callable(ctx["policy"]):
        return ctx["policy"](func, *args, **kwargs)

    # Default: call the function directly
    return func(*args, **kwargs)