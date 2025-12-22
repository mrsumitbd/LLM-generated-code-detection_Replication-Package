from typing import NamedTuple

class APIResponse(NamedTuple):
    fc_delta: str
    rc_delta: str
    tool_calls: list[tuple[str, str, str]]
    finish_reason: str | None

def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: list[tuple[str, str, io.StringIO]],
    finish_reason: str | None = None,
) -> APIResponse:
    fc_delta = _fc_delta_buffer.getvalue()
    rc_delta = _rc_delta_buffer.getvalue()
    tool_calls = [(tool_name, tool_version, buffer.getvalue()) for tool_name, tool_version, buffer in _tool_calls_buffer]
    return APIResponse(fc_delta, rc_delta, tool_calls, finish_reason)