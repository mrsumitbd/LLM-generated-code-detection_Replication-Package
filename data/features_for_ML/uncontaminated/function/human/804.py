from verifiers.types import GenerateOutputs, Messages

def _safe_last_assistant_text(messages: Messages) -> str:
    """Extract the last assistant message content if present; otherwise a short placeholder.

    Messages may be a list of dicts in chat format. Return a trimmed snippet.
    """
    try:
        if isinstance(messages, list) and messages:
            # iterate backwards to find last assistant
            for msg in reversed(messages):
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    content = msg.get("content", "") or ""
                    return _trim_snippet(str(content))
        return ""
    except Exception:
        return ""