def _safe_last_assistant_text(messages: Messages) -> str:
    if not messages:
        return "No messages available"
    
    last_assistant_message = None
    for message in reversed(messages):
        if message.get('sender') == 'assistant':
            last_assistant_message = message.get('content')
            break
    
    if last_assistant_message:
        return last_assistant_message[:50]  # Trim to first 50 characters
    else:
        return "No assistant message found"