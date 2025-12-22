import sys
from ..core import TerminalConfig, TerminalInputProvider
from .windows import WindowsTerminalProvider
from .unix import UnixTerminalProvider
from ..exceptions import TerminalUnsupportedPlatform

def create_provider(config: TerminalConfig | None = None) -> TerminalInputProvider:
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

    platform = sys.platform.lower()

    if platform.startswith("win"):
        from .windows import WindowsTerminalProvider

        return WindowsTerminalProvider(config)
    elif platform in ("linux", "darwin") or platform.startswith("freebsd"):
        from .unix import UnixTerminalProvider

        return UnixTerminalProvider(config)
    else:
        from ..exceptions import TerminalUnsupportedPlatform

        raise TerminalUnsupportedPlatform(
            platform=platform,
            operation="create_provider",
            supported_platforms=["windows", "linux", "darwin", "freebsd"],
        )