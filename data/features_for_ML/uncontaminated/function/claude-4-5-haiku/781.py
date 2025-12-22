def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: list[tuple[str, str, io.StringIO]],
    finish_reason: str | None = None,
) -> APIResponse:
    """Build an APIResponse from stream buffers."""
    fc_delta = _fc_delta_buffer.getvalue()
    rc_delta = _rc_delta_buffer.getvalue()
    
    # Build tool calls from buffer
    tool_calls = []
    for tool_id, tool_name, tool_input_buffer in _tool_calls_buffer:
        tool_input = tool_input_buffer.getvalue()
        tool_calls.append({
            "id": tool_id,
            "type": "function",
            "function": {
                "name": tool_name,
                "arguments": tool_input
            }
        })
    
    # Build content blocks
    content = []
    if fc_delta:
        content.append({
            "type": "text",
            "text": fc_delta
        })
    
    if tool_calls:
        content.append({
            "type": "tool_use",
            "tool_calls": tool_calls
        })
    
    # Build response
    response = {
        "id": "",
        "type": "message",
        "role": "assistant",
        "content": content if content else "",
        "model": "",
        "stop_reason": finish_reason,
        "stop_sequence": None,
        "usage": {
            "input_tokens": 0,
            "output_tokens": 0
        }
    }
    
    return APIResponse(response)