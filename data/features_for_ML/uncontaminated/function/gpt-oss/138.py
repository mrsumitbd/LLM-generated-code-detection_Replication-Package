import os
from enum import Enum, auto

# Try to import the real Boot enum if it exists; otherwise, provide a minimal fallback.
try:
    from .boot import Boot  # type: ignore
except Exception:
    class Boot(Enum):
        NORMAL = auto()
        BOOTLOADER = auto()
        INTERACTIVE = auto()
        SCRIPT = auto()


def _detect_boot() -> Boot:
    """
    Detect the current boot mode.

    The detection logic is intentionally simple and relies on an optional
    environment variable ``BOOT_MODE``.  If the variable is set to a value
    that matches one of the ``Boot`` enum members (case‑insensitive), that
    member is returned.  Otherwise, the function falls back to ``Boot.NORMAL``.

    This approach keeps the implementation lightweight while still allowing
    external control over the detected mode, which is useful for testing
    and for environments where the boot mode is communicated via an
    environment variable.
    """
    mode = os.getenv("BOOT_MODE")
    if mode:
        try:
            return Boot[mode.upper()]
        except Exception:
            # If the value does not correspond to a known enum member,
            # ignore it and fall back to the default.
            pass

    # Default to NORMAL if available; otherwise, return the first enum member.
    try:
        return Boot.NORMAL
    except Exception:
        return next(iter(Boot))