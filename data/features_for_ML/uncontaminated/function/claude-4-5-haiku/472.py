def _create_default_claude_code_options(
    builtin_permissions: bool = True,
    continue_conversation: bool = False,
) -> ClaudeCodeOptions:
    """Create ClaudeCodeOptions with default values.

    Args:
        builtin_permissions: Whether to include built-in permission handling defaults
    """
    return ClaudeCodeOptions(
        builtin_permissions=builtin_permissions,
        continue_conversation=continue_conversation,
    )