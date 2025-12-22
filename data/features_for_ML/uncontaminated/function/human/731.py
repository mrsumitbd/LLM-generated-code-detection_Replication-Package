import subprocess
import re

def get_cpu_info():
    # Getting platform
    os_type, avx_type, distribution = get_cpu_avx_support()

    # Getting CPU information
    cpu_info = "Unknown CPU"
    if os_type == OSType.LINUX:
        try:
            output = subprocess.check_output(["lscpu"]).decode("utf-8")
            match = re.search(r".*Model name:\s*(.+)", output)
            if match:
                cpu_info = match.group(1).strip()
            match = re.search(r".*型号名称：\s*(.+)", output)
            if match:
                cpu_info = match.group(1).strip()
        except:  # noqa
            pass
    elif os_type == OSType.DARWIN:
        try:
            output = subprocess.check_output(
                ["sysctl", "machdep.cpu.brand_string"]
            ).decode("utf-8")
            match = re.search(r"machdep.cpu.brand_string:\s*(.+)", output)
            if match:
                cpu_info = match.group(1).strip()
        except:  # noqa
            pass
    elif os_type == OSType.WINDOWS:
        try:
            output = subprocess.check_output("wmic cpu get Name", shell=True).decode(
                "utf-8"
            )
            lines = output.splitlines()
            cpu_info = lines[2].split(":")[-1].strip()
        except:  # noqa
            pass

    return os_type, avx_type, cpu_info, distribution