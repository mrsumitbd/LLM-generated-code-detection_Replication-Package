def describe_tool(tool: BaseTool) -> str:
    """Generate a description of a tool for use in prompts."""
    tool_description = f"{tool.name}: {tool.description}"
    
    if tool.args:
        args_description = ", ".join(
            f"{arg_name} ({arg_info.get('type', 'unknown')})"
            for arg_name, arg_info in tool.args.items()
        )
        tool_description += f"\n  Args: {args_description}"
    
    return tool_description