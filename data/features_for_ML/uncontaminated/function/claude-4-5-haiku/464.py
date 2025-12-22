def get_picked_tools_from_span(span: ReadableSpan) -> list[str]:
    """Extract tool names from span attributes."""
    tools = []
    
    if span.attributes is None:
        return tools
    
    # Check for common attribute names that might contain tool information
    for key in span.attributes:
        if 'tool' in key.lower():
            value = span.attributes[key]
            if isinstance(value, str):
                tools.append(value)
            elif isinstance(value, list):
                tools.extend([str(v) for v in value])
    
    # Also check for 'picked_tools' or similar direct attributes
    if 'picked_tools' in span.attributes:
        value = span.attributes['picked_tools']
        if isinstance(value, list):
            tools.extend([str(v) for v in value])
        elif isinstance(value, str):
            tools.append(value)
    
    # Check for 'tools' attribute
    if 'tools' in span.attributes:
        value = span.attributes['tools']
        if isinstance(value, list):
            tools.extend([str(v) for v in value])
        elif isinstance(value, str):
            tools.append(value)
    
    return list(dict.fromkeys(tools))  # Remove duplicates while preserving order