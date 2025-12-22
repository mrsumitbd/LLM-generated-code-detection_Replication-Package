def on_response(session, result, msg):
    """
    Handle a response from an external service or API.

    Parameters
    ----------
    session : object
        The session object that may contain state, logging, or communication
        utilities. It is expected to optionally provide a `send` method and
        a `state` attribute that can be updated with the response data.
    result : Any
        The result returned by the external call. It can be a dictionary,
        a string, or any other type.
    msg : Any
        A message that should be forwarded or logged. It can be a string,
        a dictionary, or any other type that the session's `send` method
        can handle.

    Returns
    -------
    Any
        The original `result` value is returned unchanged.
    """
    try:
        # Update session state if possible
        if hasattr(session, "state") and isinstance(session.state, dict):
            if isinstance(result, dict):
                session.state.update(result)
            else:
                session.state["last_result"] = result

        # Log the result
        if hasattr(session, "logger"):
            session.logger.info(f"Response received: {result}")
        else:
            print(f"[on_response] Response received: {result}")

        # Forward the message if provided
        if msg is not None:
            if hasattr(session, "send") and callable(session.send):
                session.send(msg)
            else:
                print(f"[on_response] Sending msg: {msg}")

    except Exception as exc:
        # If anything goes wrong, log the exception
        if hasattr(session, "logger"):
            session.logger.exception("Error in on_response")
        else:
            print(f"[on_response] Exception: {exc}")

    return result