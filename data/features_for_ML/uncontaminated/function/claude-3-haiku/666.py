import platform
import os
import sys
import subprocess

def get_installation_info() -> Dict[str, Dict[str, Any]]:
    info = {
        "system": {
            "platform": platform.system(),
            "architecture": platform.architecture()[0],
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0],
            "python_implementation": platform.python_implementation(),
            "python_compiler": platform.python_compiler(),
            "python_build": platform.python_build(),
            "os_name": os.name,
            "cwd": os.getcwd(),
            "env_vars": dict(os.environ)
        },
        "dependencies": {
            "pip_version": subprocess.check_output([sys.executable, "-m", "pip", "--version"]).decode().strip(),
            "installed_packages": {pkg.key: {"version": pkg.version, "location": pkg.location} for pkg in sorted(pkg for pkg in pkg_resources.working_set)}
        }
    }
    return info