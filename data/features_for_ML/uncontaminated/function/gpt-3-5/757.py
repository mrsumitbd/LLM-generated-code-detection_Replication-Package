def run_simulation_hpc(script_path: str) -> RunOut:
    import subprocess
    import shlex

    command = f"python {script_path}"
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return RunOut(stdout=stdout.decode(), stderr=stderr.decode(), returncode=process.returncode)