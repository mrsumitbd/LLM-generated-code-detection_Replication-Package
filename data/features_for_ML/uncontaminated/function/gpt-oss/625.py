def extract_messages(exc):
    """
    Extract a list of human‑readable messages from an exception and all of its
    chained causes or contexts.

    Parameters
    ----------
    exc : BaseException
        The exception instance to inspect.

    Returns
    -------
    list[str]
        A list of messages, starting with the outermost exception and
        proceeding through any chained exceptions.  If an exception has no
        args, its class name is used as the message.
    """
    messages = []
    seen = set()

    # Walk the exception chain: __cause__ takes precedence over __context__
    while exc is not None and exc not in seen:
        seen.add(exc)

        # Prefer the exception's args if present; otherwise use the class name
        if exc.args:
            messages.append(str(exc))
        else:
            messages.append(exc.__class__.__name__)

        # Follow the chain: __cause__ first, then __context__
        exc = exc.__cause__ or exc.__context__

    return messages