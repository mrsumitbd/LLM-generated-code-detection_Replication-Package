from nat.builder.function import Function

def _get_function_output_type(function: Function, tool_execution_config: dict[str, ToolExecutionConfig]) -> type:
    function_config = tool_execution_config.get(function.instance_name, None)
    if function_config:
        return function.streaming_output_type if function_config.use_streaming else function.single_output_type
    else:
        return function.single_output_type