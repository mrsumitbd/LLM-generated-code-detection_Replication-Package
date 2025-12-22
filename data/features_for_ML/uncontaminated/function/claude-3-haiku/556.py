import typing

def get_event_name(event: typing.Union[typing.Callable, object]) -> str:
    if callable(event):
        return event.__name__
    else:
        return event.__class__.__name__