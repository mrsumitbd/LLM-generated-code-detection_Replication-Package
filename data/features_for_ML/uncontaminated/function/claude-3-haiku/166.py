def wrapper(model):
    def inner_wrapper(*args, **kwargs):
        # Perform any pre-processing or validation on the input arguments
        result = model(*args, **kwargs)
        # Perform any post-processing or transformation on the result
        return result
    return inner_wrapper