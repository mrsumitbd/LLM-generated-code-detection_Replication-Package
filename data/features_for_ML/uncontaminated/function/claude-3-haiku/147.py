def wrapper(wrapped: Callable[P, T], instance: "Editable", args, kwargs) -> T:
    try:
        instance.before_call(wrapped.__name__, args, kwargs)
        result = wrapped(*args, **kwargs)
        instance.after_call(wrapped.__name__, args, kwargs, result)
        return result
    except Exception as e:
        instance.on_error(wrapped.__name__, args, kwargs, e)
        raise e