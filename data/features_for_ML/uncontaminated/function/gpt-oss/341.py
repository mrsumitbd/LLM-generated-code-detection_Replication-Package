from __future__ import annotations

def get_system_prompt(
    tools: list["BaseTool"],
    permission_manager: "PermissionManager",
) -> str:
    """
    Generate system prompt for the sub-agent.

    Args:
        tools: List of available tools
        permission_manager: Permission manager for checking tool access

    Returns:
        System prompt for the sub-agent
    """
    # Helper to safely get attributes
    def _get_attr(obj, name, default=""):
        return getattr(obj, name, default)

    # Build list of accessible tools
    accessible_tools = []
    for tool in tools:
        tool_name = _get_attr(tool, "name", "")
        if not tool_name:
            continue
        if permission_manager.has_permission(tool_name):
            description = _get_attr(tool, "description", "")
            if description:
                accessible_tools.append(f"- {tool_name}: {description}")
            else:
                accessible_tools.append(f"- {tool_name}")

    # Construct the prompt
    if accessible_tools:
        tools_section = "\n".join(accessible_tools)
        prompt = (
            "You are a sub-agent with access to the following tools:\n"
            f"{tools_section}\n\n"
            "Use these tools to accomplish the user's request. "
            "If you need a tool that is not listed, ask the user for permission."
        )
    else:
        prompt = (
            "You currently have no tool access. "
            "Please ask the user for permission to use any required tools."
        )

    return prompt