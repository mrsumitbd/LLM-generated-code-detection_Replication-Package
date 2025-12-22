def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: list[tuple[str, str, io.StringIO]],
    finish_reason: str | None = None,
) -> APIResponse:
    return APIResponse(_fc_delta_buffer, _rc_delta_buffer, _tool_calls_buffer, finish_reason)