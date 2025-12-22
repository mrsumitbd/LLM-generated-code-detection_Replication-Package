import os
import platform
import subprocess

class Boot:
    def __init__(self, boot_type: str, boot_time: float):
        self.boot_type = boot_type
        self.boot_time = boot_time

def _detect_boot() -> Boot:
    if platform.system() == 'Windows':
        return _detect_boot_windows()
    elif platform.system() == 'Linux':
        return _detect_boot_linux()
    elif platform.system() == 'Darwin':
        return _detect_boot_macos()
    else:
        raise NotImplementedError(f"Boot detection is not implemented for {platform.system()} platform.")

def _detect_boot_windows() -> Boot:
    boot_time = os.path.getmtime("C:\\Windows\\system32\\config\\system")
    return Boot("Windows", boot_time)

def _detect_boot_linux() -> Boot:
    output = subprocess.check_output(['who', '-b']).decode().strip()
    boot_time = float(output.split()[1])
    return Boot("Linux", boot_time)

def _detect_boot_macos() -> Boot:
    output = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).decode().strip()
    boot_time = float(output.split('=')[1].split(',')[0])
    return Boot("macOS", boot_time)