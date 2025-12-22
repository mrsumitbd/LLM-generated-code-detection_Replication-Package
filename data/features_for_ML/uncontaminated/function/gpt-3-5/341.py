def get_system_prompt(tools: list[BaseTool], permission_manager: PermissionManager) -> str:
    available_tools = [tool.name for tool in tools if permission_manager.check_access(tool)]
    return f"Available tools: {', '.join(available_tools)}" if available_tools else "No tools available"