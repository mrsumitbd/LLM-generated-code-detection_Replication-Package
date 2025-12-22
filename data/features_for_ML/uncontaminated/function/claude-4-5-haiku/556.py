import typing

def get_event_name(event: typing.Union[typing.Callable, object]) -> str:
    if isinstance(event, type):
        return event.__name__
    elif hasattr(event, '__class__'):
        return event.__class__.__name__
    elif callable(event):
        return getattr(event, '__name__', str(event))
    else:
        return str(type(event).__name__)