import json
import re

def extract_request_content(message_text: str) -> str:
    """
    Extracts the request content from a message string.

    The function attempts to locate the request content in the following order:
    1. If the message is a JSON object containing a top‑level key named "content",
       that value is returned.
    2. If the message contains a line starting with "Request:" or "Content:",
       the text following that marker (up to the end of the string) is returned.
    3. If none of the above patterns are found, the original message_text is
       returned unchanged.

    Parameters
    ----------
    message_text : str
        The raw message string from which to extract the request content.

    Returns
    -------
    str
        The extracted request content or the original message if no content
        could be identified.
    """
    # 1. Try JSON parsing
    try:
        data = json.loads(message_text)
        if isinstance(data, dict) and "content" in data:
            return str(data["content"])
    except Exception:
        pass

    # 2. Look for "Request:" or "Content:" markers
    for marker in ("Request:", "Content:"):
        idx = message_text.lower().find(marker.lower())
        if idx != -1:
            # Return everything after the marker, stripped of leading/trailing whitespace
            return message_text[idx + len(marker):].strip()

    # 3. Fallback: return the original message
    return message_text.strip()