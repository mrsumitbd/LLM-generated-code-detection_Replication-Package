def run(*args, **kwargs):
    """
    Executes a command or script with the given arguments and keyword arguments.

    Args:
        *args: Positional arguments to be passed to the command or script.
        **kwargs: Keyword arguments to be passed to the command or script.

    Returns:
        The output of the executed command or script.
    """
    import subprocess

    try:
        output = subprocess.check_output(['python'] + list(args), universal_newlines=True, **kwargs)
        return output.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None