def _create_default_claude_code_options(
    builtin_permissions: bool = True,
    continue_conversation: bool = False,
) -> ClaudeCodeOptions:
    """Create ClaudeCodeOptions with default values.

    Args:
        builtin_permissions: Whether to include built-in permission handling defaults
    """
    options = ClaudeCodeOptions(
        builtin_permissions=builtin_permissions,
        continue_conversation=continue_conversation,
        max_tokens=2048,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop_sequences=[],
    )
    return options