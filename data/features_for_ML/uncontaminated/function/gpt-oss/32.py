import os
import sys
import ctypes
from ctypes import wintypes

def enable_ansi_support():
    """
    Enable ANSI escape sequence processing on Windows consoles.
    On non-Windows platforms this function is a no-op.
    """
    if os.name != "nt":
        return

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    # Constants
    STD_OUTPUT_HANDLE = -11
    STD_ERROR_HANDLE = -12
    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    ENABLE_PROCESSED_OUTPUT = 0x0001

    def _enable(handle):
        mode = wintypes.DWORD()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING | ENABLE_PROCESSED_OUTPUT
        return kernel32.SetConsoleMode(handle, mode)

    # Enable for stdout
    stdout_handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    _enable(stdout_handle)

    # Enable for stderr
    stderr_handle = kernel32.GetStdHandle(STD_ERROR_HANDLE)
    _enable(stderr_handle)