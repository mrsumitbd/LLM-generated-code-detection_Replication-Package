def get_picked_tools_from_span(span: ReadableSpan) -> list[str]:
    picked_tools = []
    for event in span.events:
        if event.name == 'tool_picked':
            picked_tools.append(event.attributes['tool_name'])
    return picked_tools