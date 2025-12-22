import platform
import subprocess

def get_cpu_info():
    # Getting platform
    system = platform.system()
    if system == 'Windows':
        return _get_cpu_info_windows()
    elif system == 'Darwin':
        return _get_cpu_info_darwin()
    elif system == 'Linux':
        return _get_cpu_info_linux()
    else:
        return 'Unknown platform'

def _get_cpu_info_windows():
    try:
        output = subprocess.check_output(['wmic', 'cpu', 'get', 'Name'])
        cpu_name = output.decode().split('\n')[1].strip()
        return cpu_name
    except (subprocess.CalledProcessError, IndexError):
        return 'Unknown'

def _get_cpu_info_darwin():
    try:
        output = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string'])
        cpu_name = output.decode().strip()
        return cpu_name
    except subprocess.CalledProcessError:
        return 'Unknown'

def _get_cpu_info_linux():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('model name'):
                    cpu_name = line.split(':')[1].strip()
                    return cpu_name
    except (FileNotFoundError, IndexError):
        return 'Unknown'