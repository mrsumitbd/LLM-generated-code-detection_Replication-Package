import typing

def get_event_name(event: typing.Union[typing.Callable, object]) -> str:
    """
    Return a human‑readable name for an event.

    If the event is callable, the function name (or the string representation
    of the callable if it has no __name__ attribute) is returned.
    If the event is an object, the class name of the object is returned.
    """
    if callable(event):
        # Most callables (functions, methods, classes) expose a __name__ attribute.
        # Some callables (e.g., functools.partial, lambda) may not.
        try:
            return event.__name__
        except AttributeError:
            return str(event)
    else:
        return event.__class__.__name__