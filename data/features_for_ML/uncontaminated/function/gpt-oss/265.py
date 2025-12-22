import json

def _format_json_to_markdown(json_str):
    """
    Converts JSON string to a more readable markdown format.
    
    Args:
        json_str (str): JSON string to format.
    
    Returns:
        str: Formatted markdown string.
    """
    try:
        # Parse the JSON to ensure it's valid and to normalize it
        data = json.loads(json_str)
        # Pretty‑print the JSON with indentation
        pretty_json = json.dumps(data, indent=4, ensure_ascii=False)
        # Wrap in a markdown code block with language hint
        return f"```json\n{pretty_json}\n```"
    except (json.JSONDecodeError, TypeError):
        # If parsing fails, return the original string unchanged
        return json_str