import json
import io
from json_repair import repair_json
from .base_client import APIResponse, UsageRecord, BaseClient, client_registry
from ..exceptions import (
    RespParseException,
    NetworkConnectionError,
    RespNotOkException,
    ReqAbortException,
    EmptyResponseException,
)
from ..payload_content.tool_option import ToolOption, ToolParam, ToolCall

def _build_stream_api_resp(
    _fc_delta_buffer: io.StringIO,
    _rc_delta_buffer: io.StringIO,
    _tool_calls_buffer: list[tuple[str, str, io.StringIO]],
    finish_reason: str | None = None,
) -> APIResponse:
    resp = APIResponse()

    if _rc_delta_buffer.tell() > 0:
        # 如果推理内容缓冲区不为空，则将其写入APIResponse对象
        resp.reasoning_content = _rc_delta_buffer.getvalue()
    _rc_delta_buffer.close()
    if _fc_delta_buffer.tell() > 0:
        # 如果正式内容缓冲区不为空，则将其写入APIResponse对象
        resp.content = _fc_delta_buffer.getvalue()
    _fc_delta_buffer.close()
    if _tool_calls_buffer:
        # 如果工具调用缓冲区不为空，则将其解析为ToolCall对象列表
        resp.tool_calls = []
        for call_id, function_name, arguments_buffer in _tool_calls_buffer:
            if arguments_buffer.tell() > 0:
                # 如果参数串缓冲区不为空，则解析为JSON对象
                raw_arg_data = arguments_buffer.getvalue()
                arguments_buffer.close()
                try:
                    arguments = json.loads(repair_json(raw_arg_data))
                    if not isinstance(arguments, dict):
                        raise RespParseException(
                            None,
                            f"响应解析失败，工具调用参数无法解析为字典类型。工具调用参数原始响应：\n{raw_arg_data}",
                        )
                except json.JSONDecodeError as e:
                    raise RespParseException(
                        None,
                        f"响应解析失败，无法解析工具调用参数。工具调用参数原始响应：{raw_arg_data}",
                    ) from e
            else:
                arguments_buffer.close()
                arguments = None

            resp.tool_calls.append(ToolCall(call_id, function_name, arguments))

    # 检查 max_tokens 截断（流式的告警改由处理函数统一输出，这里不再输出）
    # 保留 finish_reason 仅用于上层判断
    
    if not resp.content and not resp.tool_calls:
        raise EmptyResponseException()

    return resp