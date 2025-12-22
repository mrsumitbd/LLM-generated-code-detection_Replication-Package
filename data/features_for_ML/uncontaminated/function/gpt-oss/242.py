import subprocess
import sys
import shlex

def run_command(cmd, description=None):
    """
    Execute a shell command and return its stdout.

    Parameters
    ----------
    cmd : str or list
        The command to run. If a string, it will be executed via the shell.
        If a list, it will be passed directly to subprocess.run.
    description : str, optional
        A short description of the command. If provided, it will be printed
        to stdout before the command is executed.

    Returns
    -------
    str
        The standard output of the command.

    Raises
    ------
    RuntimeError
        If the command exits with a non-zero status. The error message
        includes the command, its exit code, stdout, and stderr.
    """
    # Print description if supplied
    if description:
        print(description, file=sys.stderr)

    # Prepare the command
    if isinstance(cmd, str):
        # Use shell=True for string commands
        run_kwargs = {"shell": True, "capture_output": True, "text": True}
    else:
        # Assume list-like command
        run_kwargs = {"capture_output": True, "text": True}

    # Execute the command
    try:
        result = subprocess.run(cmd, **run_kwargs)
    except Exception as exc:
        raise RuntimeError(f"Failed to execute command: {cmd!r}") from exc

    # If the command failed, raise an error with details
    if result.returncode != 0:
        err_msg = (
            f"Command '{cmd}' exited with status {result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
        raise RuntimeError(err_msg)

    # Return the captured stdout
    return result.stdout