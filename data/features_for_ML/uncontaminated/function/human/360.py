import sys
import debugpy

def is_debugger_attached() -> bool:
    """
    Check if a debugger is attached to the current process.

    Returns
    -------
    bool
        True if a debugger is attached, False otherwise
    """
    import sys

    if "debugpy" in sys.modules:

        import debugpy

        return debugpy.is_client_connected()

    trace_func = sys.gettrace()

    # The presence of a trace function and pydevd means a debugger is attached
    if (trace_func is not None):
        trace_module = getattr(trace_func, "__module__", None)

        if (trace_module is not None and trace_module.find("pydevd") != -1):
            return True

    return False