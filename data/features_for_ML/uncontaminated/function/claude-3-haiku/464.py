def get_picked_tools_from_span(span: ReadableSpan) -> list[str]:
    tools = []
    for entity in span.entities:
        if entity.type == 'tool':
            tools.append(entity.text)
    return tools