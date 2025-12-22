import sys
import subprocess

def get_pip_command() -> list[str]:
    """
    Get the appropriate pip command for the current Python environment.
    
    Returns:
        list[str]: The pip command as a list of strings
    """
    # Try using python -m pip first (most reliable)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return [sys.executable, "-m", "pip"]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Try using pip directly
    try:
        result = subprocess.run(
            ["pip", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return ["pip"]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Try using pip3
    try:
        result = subprocess.run(
            ["pip3", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return ["pip3"]
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Default fallback
    return [sys.executable, "-m", "pip"]