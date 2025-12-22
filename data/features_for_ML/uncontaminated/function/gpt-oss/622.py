import sys
from typing import List

def get_pip_command() -> List[str]:
    """
    Return the command to invoke pip using the current Python interpreter.
    This ensures that pip runs in the same environment as the running script.
    """
    return [sys.executable, "-m", "pip"]