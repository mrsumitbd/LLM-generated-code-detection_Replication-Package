import json
import io
from typing import Any, Dict, List, Tuple, Union

# The APIResponse type is expected to be a mapping (dict) that represents a
# streaming response chunk.  If a more specific type is available in the
# surrounding codebase, replace `Dict[str, Any]` with that type.
APIResponse = Dict[str, Any]


def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: List[Tuple[str, str, io.StringIO]],
    finish_reason: Union[str, None] = None,
) -> APIResponse:
    """
    Construct a streaming API response from the provided buffers.

    Parameters
    ----------
    _fc_delta_buffer : io.StringIO
        Buffer containing the partial function call JSON (or arguments).
    _rc_delta_buffer : io.StringIO
        Buffer containing the partial response content.
    _tool_calls_buffer : list[tuple[str, str, io.StringIO]]
        List of tuples representing tool calls. Each tuple contains:
        - role (str)
        - name (str)
        - buffer (io.StringIO) with the tool call content.
    finish_reason : str | None, optional
        The finish reason for the stream, if any.

    Returns
    -------
    APIResponse
        A dictionary representing the streaming response chunk.
    """
    # Extract the current values from the buffers
    content = _rc_delta_buffer.getvalue()
    fc_raw = _fc_delta_buffer.getvalue()

    # Parse the function call buffer if possible
    function_call: Union[Dict[str, Any], None] = None
    if fc_raw:
        try:
            # Attempt to parse as JSON; if it fails, treat as raw string
            function_call = json.loads(fc_raw)
        except Exception:
            function_call = {"arguments": fc_raw}

    # Build the list of tool calls
    tool_calls: List[Dict[str, Any]] = []
    for role, name, buf in _tool_calls_buffer:
        tool_calls.append(
            {
                "role": role,
                "name": name,
                "content": buf.getvalue(),
            }
        )

    # Assemble the response dictionary
    resp: APIResponse = {
        "role": "assistant",
        "content": content,
        "function_call": function_call,
        "tool_calls": tool_calls if tool_calls else None,
        "finish_reason": finish_reason,
    }

    # Remove keys with None values to keep the payload minimal
    cleaned_resp = {k: v for k, v in resp.items() if v is not None}
    return cleaned_resp