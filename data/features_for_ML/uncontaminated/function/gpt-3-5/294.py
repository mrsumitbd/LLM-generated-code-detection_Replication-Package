def policy_fn(ctx, func, *args, **kwargs):
    if ctx.get('user_role') == 'admin':
        return func(*args, **kwargs)
    else:
        return "Access denied"