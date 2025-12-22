import os
import sys
import warnings

def warn_if_run_as_root() -> None:
    """Output a warning for sudo users on Unix.

    In a virtual environment, sudo pip still writes to virtualenv.
    On Windows, users may run pip as Administrator without issues.
    This warning only applies to Unix root users outside of virtualenv.
    """
    if os.name == 'posix' and os.geteuid() == 0 and 'VIRTUAL_ENV' not in os.environ:
        warnings.warn(
            "You are running pip as the 'root' user, which is not recommended. "
            "It is generally better to use a virtual environment instead.",
            stacklevel=2
        )