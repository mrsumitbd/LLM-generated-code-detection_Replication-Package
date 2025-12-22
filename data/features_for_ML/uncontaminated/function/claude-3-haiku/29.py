def masked_max(*args, **kwargs):
    mask = kwargs.get('mask', None)
    if mask is None:
        return max(args)
    else:
        return max(arg for arg, m in zip(args, mask) if m)