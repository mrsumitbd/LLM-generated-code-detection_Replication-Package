import shutil

def get_pip_command() -> list[str]:
    python_executable = get_pip_python_executable()
    if python_executable == _fallback_python_command:
        pip_executable = shutil.which("pip") or "pip"
        return [pip_executable]
    return [python_executable, "-m", "pip"]