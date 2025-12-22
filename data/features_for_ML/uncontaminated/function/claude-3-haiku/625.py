def extract_messages(exc):
    messages = []
    while exc:
        messages.append(str(exc))
        exc = exc.__cause__
    return messages[::-1]