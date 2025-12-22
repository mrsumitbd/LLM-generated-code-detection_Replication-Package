def _safe_last_assistant_text(messages: Messages) -> str:
    """Extract the last assistant message content if present; otherwise a short placeholder.

    Messages may be a list of dicts in chat format. Return a trimmed snippet.
    """
    if messages:
        for message in reversed(messages):
            if message.get("role") == "assistant":
                return message["content"].strip()[:100]
    return "No assistant message found."