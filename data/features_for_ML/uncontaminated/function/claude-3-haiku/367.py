def masked_min(*args, **kwargs):
    mask = kwargs.get('mask', None)
    if mask is None:
        return min(args)
    else:
        return min(arg for arg, m in zip(args, mask) if m)