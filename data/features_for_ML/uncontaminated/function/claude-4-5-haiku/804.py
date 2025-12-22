def _safe_last_assistant_text(messages: Messages) -> str:
    """Extract the last assistant message content if present; otherwise a short placeholder.

    Messages may be a list of dicts in chat format. Return a trimmed snippet.
    """
    if not messages:
        return "[no messages]"
    
    # Iterate backwards through messages to find the last assistant message
    for message in reversed(messages):
        if isinstance(message, dict) and message.get("role") == "assistant":
            content = message.get("content", "")
            if isinstance(content, str):
                # Trim to a reasonable length and strip whitespace
                trimmed = content.strip()
                if len(trimmed) > 100:
                    trimmed = trimmed[:97] + "..."
                return trimmed if trimmed else "[empty message]"
            return "[non-string content]"
    
    return "[no assistant message]"