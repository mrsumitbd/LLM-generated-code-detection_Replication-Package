def _format_json_to_markdown(json_str):
    """
    Converts JSON string to a more readable markdown format.
    
    Args:
        json_str (str): JSON string to format.
    
    Returns:
        str: Formatted markdown string.
    """
    import json
    
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        return "Invalid JSON string."
    
    def _format_value(value, indent=0):
        if isinstance(value, dict):
            return _format_dict(value, indent)
        elif isinstance(value, list):
            return _format_list(value, indent)
        else:
            return f"{' ' * indent}- {value}"
    
    def _format_dict(d, indent=0):
        lines = []
        for key, value in d.items():
            lines.append(f"{' ' * indent}**{key}:**")
            lines.append(_format_value(value, indent + 2))
        return "\n".join(lines)
    
    def _format_list(l, indent=0):
        lines = []
        for item in l:
            lines.append(_format_value(item, indent + 2))
        return "\n".join(lines)
    
    return _format_value(data)