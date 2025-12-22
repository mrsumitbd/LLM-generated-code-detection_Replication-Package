import os
from transformers.utils.hub import TRANSFORMERS_CACHE

def patch_transformers_module_dir(env_vars: dict[str, str]):
    from transformers.utils.hub import TRANSFORMERS_CACHE

    module_dir = os.path.join(TRANSFORMERS_CACHE, "..", "modules")
    assert module_dir is not None, "TRANSFORMERS_CACHE should exist."
    if "PYTHONPATH" not in env_vars:
        env_vars["PYTHONPATH"] = module_dir
    else:
        env_vars["PYTHONPATH"] = f"{module_dir}:{env_vars['PYTHONPATH']}"

    return env_vars