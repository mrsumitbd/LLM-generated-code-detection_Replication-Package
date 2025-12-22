def get_cpu_info():
    # Getting platform
    import platform
    import subprocess
    import os
    
    cpu_info = {}
    
    # Get processor name
    try:
        if platform.system() == "Windows":
            cpu_info['processor'] = platform.processor()
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                  capture_output=True, text=True)
            cpu_info['processor'] = result.stdout.strip()
        else:  # Linux
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('model name'):
                        cpu_info['processor'] = line.split(':', 1)[1].strip()
                        break
    except:
        cpu_info['processor'] = "Unknown"
    
    # Get number of cores
    try:
        cpu_info['cores'] = os.cpu_count()
    except:
        cpu_info['cores'] = "Unknown"
    
    # Get architecture
    try:
        cpu_info['architecture'] = platform.machine()
    except:
        cpu_info['architecture'] = "Unknown"
    
    # Get platform
    try:
        cpu_info['platform'] = platform.system()
    except:
        cpu_info['platform'] = "Unknown"
    
    return cpu_info