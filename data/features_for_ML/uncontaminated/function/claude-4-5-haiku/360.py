import sys

def is_debugger_attached() -> bool:
    """
    Check if a debugger is attached to the current process.

    Returns
    -------
    bool
        True if a debugger is attached, False otherwise
    """
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None