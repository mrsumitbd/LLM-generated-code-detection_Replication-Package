from typing import Union
import io

def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: list[tuple[str, str, io.StringIO]],
    finish_reason: Union[str, None] = None,
) -> APIResponse:
    # Implementation goes here
    pass