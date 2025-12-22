import os
import sys
import platform
import warnings

def warn_if_run_as_root() -> None:
    """Output a warning for sudo users on Unix.

    In a virtual environment, sudo pip still writes to virtualenv.
    On Windows, users may run pip as Administrator without issues.
    This warning only applies to Unix root users outside of virtualenv.
    """
    # Only relevant on POSIX systems
    if os.name != "posix":
        return

    # Check if running as root
    try:
        is_root = os.geteuid() == 0
    except AttributeError:
        # os.geteuid not available (unlikely on posix, but guard anyway)
        return

    if not is_root:
        return

    # Detect virtual environment
    # 1. Check VIRTUAL_ENV env var
    in_virtualenv = bool(os.getenv("VIRTUAL_ENV"))
    # 2. Check sys.prefix vs sys.base_prefix (Python 3.3+)
    if not in_virtualenv and hasattr(sys, "base_prefix"):
        in_virtualenv = sys.prefix != sys.base_prefix

    if in_virtualenv:
        return

    # Emit warning
    warnings.warn(
        "You are running pip as root. This is not recommended. "
        "Consider using a virtual environment or running pip with --user.",
        RuntimeWarning,
    )