import os
import sys

def patch_transformers_module_dir(env_vars: dict[str, str]):
    """
    Patches the transformers module directory to use the specified environment variables.

    Args:
        env_vars (dict[str, str]): A dictionary of environment variables to use for the transformers module directory.
    """
    transformers_module_dir = env_vars.get("TRANSFORMERS_MODULE_DIR", None)
    if transformers_module_dir:
        sys.path.insert(0, transformers_module_dir)
        os.environ["TRANSFORMERS_MODULE_DIR"] = transformers_module_dir