import anthropic


def extract_messages(exc):
    """
    Extract messages from an Anthropic API exception.
    
    Args:
        exc: An exception object from the Anthropic API
        
    Returns:
        A list of message strings extracted from the exception
    """
    messages = []
    
    # Check if exception has a message attribute
    if hasattr(exc, 'message'):
        messages.append(exc.message)
    
    # Check if exception has args
    if hasattr(exc, 'args') and exc.args:
        for arg in exc.args:
            if isinstance(arg, str):
                messages.append(arg)
            elif isinstance(arg, dict):
                # Handle dict arguments that might contain error details
                if 'message' in arg:
                    messages.append(arg['message'])
                elif 'error' in arg:
                    error = arg['error']
                    if isinstance(error, dict) and 'message' in error:
                        messages.append(error['message'])
                    else:
                        messages.append(str(error))
    
    # Check for response attribute (common in HTTP exceptions)
    if hasattr(exc, 'response'):
        response = exc.response
        if hasattr(response, 'text'):
            messages.append(response.text)
        elif hasattr(response, 'content'):
            messages.append(str(response.content))
    
    # Check for body attribute (Anthropic specific)
    if hasattr(exc, 'body'):
        body = exc.body
        if isinstance(body, dict):
            if 'error' in body:
                error = body['error']
                if isinstance(error, dict) and 'message' in error:
                    messages.append(error['message'])
                else:
                    messages.append(str(error))
            elif 'message' in body:
                messages.append(body['message'])
        else:
            messages.append(str(body))
    
    # Fallback to string representation
    if not messages:
        messages.append(str(exc))
    
    # Remove duplicates while preserving order
    seen = set()
    unique_messages = []
    for msg in messages:
        if msg and msg not in seen:
            seen.add(msg)
            unique_messages.append(msg)
    
    return unique_messages