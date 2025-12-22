import sys

def is_debugger_attached() -> bool:
    """
    Check if a debugger is attached to the current process.

    Returns
    -------
    bool
        True if a debugger is attached, False otherwise
    """
    # sys.gettrace() returns a trace function when a debugger is active.
    # It returns None when no debugger is attached.
    return sys.gettrace() is not None