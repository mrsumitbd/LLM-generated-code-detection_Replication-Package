def extract_messages(exc):
    messages = []
    current = exc
    while current:
        if hasattr(current, 'message'):
            messages.append(current.message)
        current = current.__cause__
    return messages