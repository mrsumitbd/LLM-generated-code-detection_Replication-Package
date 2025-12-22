def _safe_last_assistant_text(messages: Messages) -> str:
    """
    Extract the last assistant message content if present; otherwise a short placeholder.

    Messages may be a list of dicts in chat format. Return a trimmed snippet.
    """
    if not messages:
        return "No assistant message found."

    # Iterate from the end to find the most recent assistant message
    for msg in reversed(messages):
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            content = msg.get("content", "")
            if not isinstance(content, str):
                content = str(content)
            snippet = content.strip()
            # Trim to a reasonable length (200 chars) with ellipsis if needed
            if len(snippet) > 200:
                snippet = snippet[:197] + "..."
            return snippet

    # No assistant message found
    return "No assistant message found."