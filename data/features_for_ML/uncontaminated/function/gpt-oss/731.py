import platform
import os
import sys

def get_cpu_info():
    """
    Return a dictionary containing basic CPU information.
    """
    info = {}

    # Basic platform information
    info['processor'] = platform.processor()
    info['machine'] = platform.machine()
    info['platform'] = platform.platform()

    # CPU counts
    try:
        info['logical_cores'] = os.cpu_count()
    except Exception:
        info['logical_cores'] = None

    # Physical cores (if psutil is available)
    try:
        import psutil
        info['physical_cores'] = psutil.cpu_count(logical=False)
        # CPU frequency
        freq = psutil.cpu_freq()
        if freq:
            info['max_frequency_mhz'] = freq.max
            info['min_frequency_mhz'] = freq.min
            info['current_frequency_mhz'] = freq.current
        else:
            info['max_frequency_mhz'] = None
            info['min_frequency_mhz'] = None
            info['current_frequency_mhz'] = None
        # CPU usage per core
        try:
            usage = psutil.cpu_percent(percpu=True, interval=0.1)
            info['cpu_usage_percent_per_core'] = usage
        except Exception:
            info['cpu_usage_percent_per_core'] = None
    except ImportError:
        # psutil not available; use fallback
        info['physical_cores'] = None
        info['max_frequency_mhz'] = None
        info['min_frequency_mhz'] = None
        info['current_frequency_mhz'] = None
        info['cpu_usage_percent_per_core'] = None

    return info