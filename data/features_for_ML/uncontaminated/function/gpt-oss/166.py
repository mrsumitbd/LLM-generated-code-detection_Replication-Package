def wrapper(model):
    def wrapped(*args, **kwargs):
        return model(*args, **kwargs)
    return wrapped