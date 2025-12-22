import sys
from typing import Union

from .config import TerminalConfig
from .providers import TerminalInputProvider, WindowsTerminalProvider, UnixTerminalProvider, DummyTerminalProvider

def create_provider(config: Union[TerminalConfig, None] = None) -> TerminalInputProvider:
    """Create appropriate terminal provider for current platform.

    Args:
        config: Terminal configuration, uses defaults if None

    Returns:
        Platform-specific terminal provider

    Raises:
        TerminalUnsupportedPlatform: If platform is not supported
    """
    if config is None:
        config = TerminalConfig()

    if sys.platform.startswith("win"):
        return WindowsTerminalProvider(config)
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        return UnixTerminalProvider(config)
    else:
        return DummyTerminalProvider(config)