import json
from opentelemetry.sdk.trace import ReadableSpan

def get_picked_tools_from_span(span: ReadableSpan) -> list[str]:
    if not span.attributes:
        return []

    if not (events := span.attributes.get("events")):
        return []

    if not isinstance(events, str):
        return []

    deserialized_events = json.loads(events)

    assistant_event = deserialized_events[-1]

    if not (message := assistant_event.get("message")):
        return []

    if not (tool_calls := message.get("tool_calls")):
        return []

    return [
        tool_call.get(
            "function",
            {},
        ).get(
            "name",
            "<unknown>",
        )
        for tool_call in tool_calls
        if tool_call.get("type") == "function"
    ]