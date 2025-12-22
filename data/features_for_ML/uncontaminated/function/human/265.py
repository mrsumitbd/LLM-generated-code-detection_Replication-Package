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
        data = json.loads(json_str)
        if isinstance(data, dict):
            return "\n".join([f"- **{k}**: {v}" for k, v in data.items()])
        elif isinstance(data, list):
            return "\n".join([f"- {item}" for item in data])
        return str(data)
    except:
        return json_str