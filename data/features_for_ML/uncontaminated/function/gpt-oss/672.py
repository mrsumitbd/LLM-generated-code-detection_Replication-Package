import json
from typing import Any, List, Union

def get_fixed_tool_calls_or_text_output(json_str: str, max_depth: int = 5) -> Union[List[Any], str]:
    """
    Parse a JSON string that may contain tool calls or plain text output.
    The function attempts to extract the first occurrence of either a list of
    tool calls (under the key "tool_calls") or a text string (under the key
    "content").  Nested structures are traversed up to `max_depth`.  If the
    string cannot be parsed as JSON or no relevant key is found, the original
    string is returned unchanged.

    Parameters
    ----------
    json_str : str
        The JSON string to parse.
    max_depth : int, default 5
        Maximum recursion depth when searching nested structures.

    Returns
    -------
    Union[List[Any], str]
        Either a list of tool call objects, a text string, or the original
        string if parsing fails or no relevant key is found.
    """
    try:
        data = json.loads(json_str)
    except Exception:
        # Not valid JSON – return the original string
        return json_str

    def _extract(obj: Any, depth: int) -> Any:
        if depth > max_depth:
            return None

        if isinstance(obj, dict):
            # Direct tool calls
            if "tool_calls" in obj:
                return _extract(obj["tool_calls"], depth + 1)

            # Direct content string
            if "content" in obj:
                return obj["content"]

            # Search recursively in all values
            for value in obj.values():
                result = _extract(value, depth + 1)
                if result is not None:
                    return result

        elif isinstance(obj, list):
            # Collect all non-None results from the list
            results = []
            for item in obj:
                result = _extract(item, depth + 1)
                if result is not None:
                    results.append(result)
            if results:
                return results

        else:
            # Primitive value – return as is
            return obj

        return None

    extracted = _extract(data, 0)

    # If extraction failed, return the original string
    if extracted is None:
        return json_str

    return extracted