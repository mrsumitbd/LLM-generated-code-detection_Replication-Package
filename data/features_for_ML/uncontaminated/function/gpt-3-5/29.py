def masked_max(*args, **kwargs):
    mask = kwargs.get('mask', None)
    filtered_args = [arg for arg in args if mask is None or arg != mask]
    return max(filtered_args) if filtered_args else None