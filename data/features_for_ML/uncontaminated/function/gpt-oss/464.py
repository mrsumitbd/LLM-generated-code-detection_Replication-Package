import json
from typing import List

def get_picked_tools_from_span(span) -> List[str]:
    """
    Extract the names of tools that were invoked in the given span.

    The function looks for tool call information in two places:
    1. Span attributes under the key "tool_calls" (JSON string or list).
    2. Span events named "tool_call" with an attribute "name".

    Parameters
    ----------
    span : ReadableSpan
        The span to inspect. It is expected to expose an `attributes` dict
        and an `events` iterable of objects with `name` and `attributes`.

    Returns
    -------
    List[str]
        A list of tool names that were called in the span.
    """
    tool_names: List[str] = []

    # 1. Check span attributes for a "tool_calls" entry
    tool_calls_attr = getattr(span, "attributes", {}).get("tool_calls")
    if tool_calls_attr:
        # The attribute might be a JSON string or a list of dicts
        if isinstance(tool_calls_attr, str):
            try:
                tool_calls = json.loads(tool_calls_attr)
            except json.JSONDecodeError:
                tool_calls = []
        else:
            tool_calls = tool_calls_attr

        if isinstance(tool_calls, list):
            for call in tool_calls:
                if isinstance(call, dict):
                    name = call.get("name")
                    if isinstance(name, str):
                        tool_names.append(name)

    # 2. Check span events for tool calls
    for event in getattr(span, "events", []):
        if getattr(event, "name", None) == "tool_call":
            event_attrs = getattr(event, "attributes", {})
            name = event_attrs.get("name")
            if isinstance(name, str):
                tool_names.append(name)

    # Remove duplicates while preserving order
    seen = set()
    unique_tool_names = []
    for name in tool_names:
        if name not in seen:
            seen.add(name)
            unique_tool_names.append(name)

    return unique_tool_names