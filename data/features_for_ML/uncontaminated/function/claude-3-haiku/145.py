def _get_function_output_type(function: Function, tool_execution_config: dict[str, ToolExecutionConfig]) -> type:
    """
    Determines the output type of the given function based on the tool execution configuration.

    Args:
        function (Function): The function to get the output type for.
        tool_execution_config (dict[str, ToolExecutionConfig]): The tool execution configuration.

    Returns:
        type: The output type of the function.
    """
    tool_config = tool_execution_config.get(function.__name__, None)
    if tool_config is None:
        return type(None)

    return tool_config.output_type