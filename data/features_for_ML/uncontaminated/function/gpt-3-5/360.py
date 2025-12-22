import ctypes

def is_debugger_attached() -> bool:
    kernel32 = ctypes.windll.kernel32
    return kernel32.IsDebuggerPresent() != 0