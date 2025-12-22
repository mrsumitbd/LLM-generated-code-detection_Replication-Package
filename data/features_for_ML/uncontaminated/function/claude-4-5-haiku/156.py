def _custom_policy(ctx, func, *args, **kwargs):
    """Execute a function with a custom policy context."""
    if ctx is None:
        return func(*args, **kwargs)
    
    # Store the current policy context
    old_ctx = getattr(_thread_local, 'policy_ctx', None)
    
    try:
        # Set the new policy context
        _thread_local.policy_ctx = ctx
        # Execute the function with the new context
        return func(*args, **kwargs)
    finally:
        # Restore the old policy context
        if old_ctx is None:
            if hasattr(_thread_local, 'policy_ctx'):
                delattr(_thread_local, 'policy_ctx')
        else:
            _thread_local.policy_ctx = old_ctx