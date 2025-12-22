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
    tool_descriptions = []
    for tool in tools:
        if permission_manager.can_use(tool):
            tool_descriptions.append(f"- {tool.name}: {tool.description}")

    system_prompt = (
        "You are an AI assistant created by Anthropic to be helpful, harmless, and honest.\n"
        "You have access to the following tools:\n"
        "\n"
        + "\n".join(tool_descriptions)
        + "\n\n"
        "Use these tools to assist the user to the best of your abilities, while staying within the bounds of your ethical training and the user's instructions."
    )

    return system_prompt