import os
import sys
import json
import subprocess
from typing import List

# Try to import the real SysValues definition; fall back to a minimal one if unavailable.
try:
    from pipask.sys_values import SysValues
except Exception:  # pragma: no cover
    from dataclasses import dataclass

    @dataclass
    class SysValues:
        version: str
        executable: str
        prefix: str
        base_prefix: str
        base_exec_prefix: str
        path: List[str]


def _run_target_python(script: str, python_executable: str) -> str:
    """Run a small Python script with the target interpreter and return its stdout."""
    result = subprocess.run(
        [python_executable, "-c", script],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_pip_sys_values() -> SysValues:
    """
    Returns various sys values as they are in the *target* environment.
    This is because pipask is typically installed in a different environment (e.g., pipx)
    than the installation target environment.
    """
    # Determine the target Python executable.
    # Prefer the environment variable if set; otherwise fall back to the current interpreter.
    target_python = os.getenv("PIPASK_TARGET_PYTHON", sys.executable)

    # Script that prints the desired sys attributes as JSON.
    script = """
import sys, json
data = {
    "version": sys.version,
    "executable": sys.executable,
    "prefix": sys.prefix,
    "base_prefix": sys.base_prefix,
    "base_exec_prefix": sys.base_exec_prefix,
    "path": sys.path,
}
print(json.dumps(data))
"""

    output = _run_target_python(script, target_python)
    data = json.loads(output)

    # Construct and return the SysValues instance.
    return SysValues(
        version=data["version"],
        executable=data["executable"],
        prefix=data["prefix"],
        base_prefix=data["base_prefix"],
        base_exec_prefix=data["base_exec_prefix"],
        path=data["path"],
    )