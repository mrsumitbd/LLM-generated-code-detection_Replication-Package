def wrapper(model):
    def inner(*args, **kwargs):
        print("Before calling the model")
        result = model(*args, **kwargs)
        print("After calling the model")
        return result
    return inner