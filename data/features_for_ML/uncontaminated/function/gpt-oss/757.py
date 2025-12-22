import subprocess
import sys
from pathlib import Path
from typing import Any

# Try to import RunOut from the surrounding package; if it doesn't exist,
# define a minimal fallback dataclass.
try:
    from .runout import RunOut  # type: ignore
except Exception:  # pragma: no cover
    from dataclasses import dataclass

    @dataclass
    class RunOut:
        stdout: str
        stderr: str
        returncode: int


def run_simulation_hpc(script_path: str) -> RunOut:
    """
    Execute a simulation script on an HPC node.

    Parameters
    ----------
    script_path : str
        Path to the script to run. The script is executed using the current
        Python interpreter.

    Returns
    -------
    RunOut
        An object containing the captured stdout, stderr, and the return code.
    """
    # Resolve the script path
    script = Path(script_path).expanduser().resolve()
    if not script.is_file():
        raise FileNotFoundError(f"Script not found: {script}")

    # Build the command: use the current Python interpreter
    cmd = [sys.executable, str(script)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # We want to capture the return code even on failure
        )
        return RunOut(
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
        )
    except Exception as exc:  # pragma: no cover
        # In case of an unexpected exception, return it in stderr
        return RunOut(
            stdout="",
            stderr=str(exc),
            returncode=-1,
        )