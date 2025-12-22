import typing

def get_event_name(event: typing.Union[typing.Callable, object]) -> str:
    if hasattr(event, "__name__"):
        return event.__name__
    return event.__class__.__name__