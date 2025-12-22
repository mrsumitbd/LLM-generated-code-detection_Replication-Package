from claude_code_sdk import ClaudeCodeOptions

def _create_default_claude_code_options(
    builtin_permissions: bool = True,
    continue_conversation: bool = False,
) -> ClaudeCodeOptions:
    """Create ClaudeCodeOptions with default values.

    Args:
        builtin_permissions: Whether to include built-in permission handling defaults
    """
    if builtin_permissions:
        return ClaudeCodeOptions(
            continue_conversation=continue_conversation,
            mcp_servers={
                "confirmation": {"type": "sse", "url": "http://127.0.0.1:8000/mcp"}
            },
            permission_prompt_tool_name="mcp__confirmation__check_permission",
        )
    else:
        return ClaudeCodeOptions(
            mcp_servers={},
            permission_prompt_tool_name=None,
            continue_conversation=continue_conversation,
        )