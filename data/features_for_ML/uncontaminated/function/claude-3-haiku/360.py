import sys
import os

def is_debugger_attached() -> bool:
    """
    Check if a debugger is attached to the current process.

    Returns
    -------
    bool
        True if a debugger is attached, False otherwise
    """
    if sys.platform.startswith("win"):
        import ctypes
        kernel32 = ctypes.windll.kernel32
        return kernel32.IsDebuggerPresent() != 0
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        try:
            pid = os.getpid()
            proc_status = f"/proc/{pid}/status"
            with open(proc_status, "r") as f:
                for line in f:
                    if line.startswith("TracerPid:"):
                        return int(line.split(":")[1]) > 0
        except (OSError, ValueError):
            pass
    return False