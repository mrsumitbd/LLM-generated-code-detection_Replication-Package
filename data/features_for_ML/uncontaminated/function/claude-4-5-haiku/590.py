def create_provider(config: TerminalConfig | None = None) -> TerminalInputProvider:
    """Create appropriate terminal provider for current platform.

    Args:
        config: Terminal configuration, uses defaults if None

    Returns:
        Platform-specific terminal provider

    Raises:
        TerminalUnsupportedPlatform: If platform is not supported
    """
    import sys
    import platform
    
    if config is None:
        config = TerminalConfig()
    
    system = platform.system()
    
    if system == "Windows":
        return WindowsTerminalInputProvider(config)
    elif system == "Darwin":
        return UnixTerminalInputProvider(config)
    elif system == "Linux":
        return UnixTerminalInputProvider(config)
    else:
        raise TerminalUnsupportedPlatform(f"Platform '{system}' is not supported")