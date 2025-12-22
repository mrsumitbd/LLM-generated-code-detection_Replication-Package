import subprocess
import json
from typing import Dict, Any

def get_installation_info() -> Dict[str, Dict[str, Any]]:
    """Get installation information for Python packages using pip."""
    result = subprocess.run(
        ["pip", "list", "--format", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    
    packages = json.loads(result.stdout)
    
    installation_info = {}
    for package in packages:
        name = package["name"]
        version = package["version"]
        installation_info[name] = {
            "version": version,
            "location": None
        }
    
    result = subprocess.run(
        ["pip", "show", "-f"] + list(installation_info.keys()),
        capture_output=True,
        text=True
    )
    
    current_package = None
    for line in result.stdout.split("\n"):
        if line.startswith("Name: "):
            current_package = line.split("Name: ")[1].strip()
        elif line.startswith("Location: ") and current_package:
            location = line.split("Location: ")[1].strip()
            if current_package in installation_info:
                installation_info[current_package]["location"] = location
    
    return installation_info