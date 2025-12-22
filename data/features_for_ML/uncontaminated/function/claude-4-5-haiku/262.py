def warn_if_run_as_root() -> None:
    """Output a warning for sudo users on Unix.

    In a virtual environment, sudo pip still writes to virtualenv.
    On Windows, users may run pip as Administrator without issues.
    This warning only applies to Unix root users outside of virtualenv.
    """
    import os
    import sys
    
    # Check if running on Unix-like system and as root
    if os.name != 'nt' and os.getuid() == 0:
        # Check if we're in a virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            import warnings
            warnings.warn(
                "Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. "
                "It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv",
                stacklevel=2
            )