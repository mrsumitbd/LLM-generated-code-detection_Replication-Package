def create_provider(config: TerminalConfig | None = None) -> TerminalInputProvider:
    if config is None:
        config = TerminalConfig()

    if sys.platform == 'win32':
        return WindowsTerminalProvider(config)
    elif sys.platform == 'darwin':
        return DarwinTerminalProvider(config)
    elif sys.platform.startswith('linux'):
        return LinuxTerminalProvider(config)
    else:
        raise TerminalUnsupportedPlatform("Platform not supported")