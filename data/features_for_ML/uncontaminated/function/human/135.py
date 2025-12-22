def wrapper(*args, **kwargs):  # noqa: ANN202
        if is_rank0():
            result = func(*args, **kwargs)
        barrier()
        if not is_rank0():
            result = func(*args, **kwargs)
        return result