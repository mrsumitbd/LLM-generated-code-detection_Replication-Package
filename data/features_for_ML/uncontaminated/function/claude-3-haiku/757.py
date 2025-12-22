from typing import NamedTuple

class RunOut(NamedTuple):
    exit_code: int
    stdout: str
    stderr: str

import subprocess

def run_simulation_hpc(script_path: str) -> RunOut:
    try:
        result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        return RunOut(result.returncode, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        return RunOut(e.returncode, e.stdout, e.stderr)