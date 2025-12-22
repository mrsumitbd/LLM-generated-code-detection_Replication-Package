def on_response(session, result, msg):
    """
    Handle a response from a session.
    
    Args:
        session: The session object
        result: The result of the operation
        msg: The message associated with the response
    """
    if session is None:
        return
    
    if result is None:
        return
    
    if msg is None:
        msg = ""
    
    try:
        if hasattr(session, 'on_response'):
            session.on_response(result, msg)
        elif hasattr(session, 'handle_response'):
            session.handle_response(result, msg)
        else:
            pass
    except Exception as e:
        pass