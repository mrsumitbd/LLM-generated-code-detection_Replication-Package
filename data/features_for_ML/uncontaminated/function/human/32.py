import ctypes
from ctypes import wintypes
import sys

def enable_ansi_support():
    if sys.platform != "win32":
        return  # 非Windows系统无需处理

    # 调用Windows API启用虚拟终端处理
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    handle = kernel32.GetStdHandle(wintypes.DWORD(-11))  # STD_OUTPUT_HANDLE (-11)
    mode = wintypes.DWORD()
    if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
        return
    # 启用 ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
    if not kernel32.SetConsoleMode(handle, mode.value | 0x0004):
        return