from mcp_claude_code.tools.common.base import BaseTool
from mcp_claude_code.tools.common.permissions import PermissionManager

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
    # Get filtered tools
    filtered_tools = get_allowed_agent_tools(tools, permission_manager)

    # Extract tool names for display
    tool_names = ", ".join(f"`{tool.name}`" for tool in filtered_tools)

    # Base system prompt
    system_prompt = f"""You are a sub-agent assistant with access to these tools: {tool_names}.

GUIDELINES:
1. You work autonomously - you cannot ask follow-up questions
2. You have access to read-only tools - you cannot modify files or execute commands
3. Your response is returned directly to the main assistant, not the user
4. Be concise and focus on the specific task assigned
5. When relevant, share file names and code snippets relevant to the query
6. Any file paths you return in your final response MUST be absolute. DO NOT use relative paths.
7. CRITICAL: You can only work with the absolute paths provided in your task prompt. You cannot infer or guess other locations.

RESPONSE FORMAT:
- Begin with a summary of findings
- Include relevant details and context
- Organize information logically
- End with clear conclusions
"""

    return system_prompt