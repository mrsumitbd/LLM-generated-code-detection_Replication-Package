import sys

def get_pip_command() -> list[str]:
    if sys.version_info.major == 3 and sys.version_info.minor >= 4:
        return [sys.executable, "-m", "pip"]
    else:
        return [sys.executable, "-m", "pip3"]