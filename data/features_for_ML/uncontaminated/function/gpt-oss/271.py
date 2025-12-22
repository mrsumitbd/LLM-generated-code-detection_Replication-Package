import os

def patch_transformers_module_dir(env_vars: dict[str, str]) -> None:
    """
    Ensure that the environment variable `TRANSFORMERS_MODULE_DIR` is set to the
    absolute path of the local `transformers` module directory. If the variable
    is already present, it is left untouched.

    The function looks for a directory named `transformers` in the current
    working directory. If found, that directory is used; otherwise the current
    working directory itself is used as a fallback.

    Parameters
    ----------
    env_vars : dict[str, str]
        Dictionary of environment variables that will be passed to a subprocess.
    """
    # Do nothing if the variable is already defined
    if "TRANSFORMERS_MODULE_DIR" in env_vars:
        return

    cwd = os.getcwd()
    candidate = os.path.join(cwd, "transformers")

    if os.path.isdir(candidate):
        env_vars["TRANSFORMERS_MODULE_DIR"] = os.path.abspath(candidate)
    else:
        # Fallback to the current working directory if no explicit module dir
        env_vars["TRANSFORMERS_MODULE_DIR"] = cwd