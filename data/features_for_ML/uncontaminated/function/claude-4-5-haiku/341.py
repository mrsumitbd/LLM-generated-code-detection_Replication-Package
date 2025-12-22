def get_system_prompt(
    tools: list[BaseTool],
    permission_manager: PermissionManager,
) -> str:
    """Generate system prompt for the sub-agent.

    Args:
        tools: List of available tools
        permission_manager: Permission manager for checking tool access

    Returns:
        System prompt for the sub-agent
    """
    available_tools = []
    
    for tool in tools:
        if permission_manager.has_access(tool.name):
            tool_info = f"- {tool.name}: {tool.description}"
            if hasattr(tool, 'args_schema') and tool.args_schema:
                tool_info += f"\n  Args: {tool.args_schema}"
            available_tools.append(tool_info)
    
    tools_section = "\n".join(available_tools) if available_tools else "No tools available"
    
    system_prompt = f"""You are a helpful sub-agent assistant. You have access to the following tools:

{tools_section}

Use these tools to help accomplish tasks. Always consider the user's request and use the appropriate tools when needed. Be clear about what you're doing and provide helpful responses."""
    
    return system_prompt