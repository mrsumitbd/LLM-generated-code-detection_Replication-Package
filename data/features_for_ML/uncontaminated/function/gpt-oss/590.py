import sys
from typing import TYPE_CHECKING

from .config import TerminalConfig
from .exceptions import TerminalUnsupportedPlatform
from .providers import UnixTerminalProvider, WindowsTerminalProvider

if TYPE_CHECKING:
    from .providers import TerminalInputProvider


def create_provider(config: TerminalConfig | None = None) -> "TerminalInputProvider":
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

    platform_name = sys.platform.lower()

    if platform_name.startswith("win"):
        return WindowsTerminalProvider(config)
    if platform_name.startswith(("linux", "darwin", "freebsd", "openbsd", "netbsd")):
        return UnixTerminalProvider(config)

    raise TerminalUnsupportedPlatform(f"Unsupported platform: {platform_name}")