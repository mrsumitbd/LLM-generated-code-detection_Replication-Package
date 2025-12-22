def wrapper(*args, **kwargs):  # noqa: ANN202
        if is_rank0():
            return func(*args, **kwargs)
        else:
            return None