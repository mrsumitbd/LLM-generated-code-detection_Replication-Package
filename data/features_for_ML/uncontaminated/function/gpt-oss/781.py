import io
from typing import Any, Dict, List, Tuple, Union

# Assuming APIResponse is a dict-like type used by the surrounding code.
APIResponse = Dict[str, Any]

def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: List[Tuple[str, str, io.StringIO]],
    finish_reason: Union[str, None] = None,
) -> APIResponse:
    """
    Build a streaming API response dictionary from the provided buffers.

    Parameters
    ----------
    _fc_delta_buffer : io.StringIO
        Buffer containing the function call arguments (if any).
    _rc_delta_buffer : io.StringIO
        Buffer containing the response content (if any).
    _tool_calls_buffer : list[tuple[str, str, io.StringIO]]
        List of tuples representing tool calls. Each tuple contains:
        - role: the role of the tool call (e.g., "tool").
        - name: the name of the tool.
        - buffer: a StringIO buffer containing the tool arguments.
    finish_reason : str | None, optional
        The finish reason for the completion, if any.

    Returns
    -------
    APIResponse
        A dictionary representing the streaming API response.
    """
    # Extract the accumulated strings from the buffers
    rc_content = _rc_delta_buffer.getvalue()
    fc_args = _fc_delta_buffer.getvalue()

    # Build the tool calls list
    tool_calls: List[Dict[str, Any]] = []
    for idx, (role, name, buf) in enumerate(_tool_calls_buffer):
        args = buf.getvalue()
        tool_calls.append(
            {
                "id": f"tool_{idx}",
                "type": role,
                "function": {"name": name, "arguments": args},
            }
        )

    # Construct the delta dictionary
    delta: Dict[str, Any] = {}
    if rc_content:
        delta["content"] = rc_content
    if fc_args:
        # If the function name is known elsewhere, it can be added here.
        # For now, we include only the arguments.
        delta["function_call"] = {"arguments": fc_args}
    if tool_calls:
        delta["tool_calls"] = tool_calls

    # Build the choice entry
    choice: Dict[str, Any] = {"delta": delta, "index": 0}
    if finish_reason is not None:
        choice["finish_reason"] = finish_reason

    # Return the final APIResponse structure
    return {"choices": [choice]}