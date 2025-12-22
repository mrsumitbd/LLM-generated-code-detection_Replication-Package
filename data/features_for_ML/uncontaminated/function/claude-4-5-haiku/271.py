import os
import sys
from pathlib import Path
from contextlib import contextmanager

def patch_transformers_module_dir(env_vars: dict[str, str]):
    """
    Patches the transformers module directory by setting environment variables
    and ensuring the module can be imported from the specified location.
    """
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    # If TRANSFORMERS_MODULE_DIR is set, ensure it's in the Python path
    if 'TRANSFORMERS_MODULE_DIR' in env_vars:
        module_dir = env_vars['TRANSFORMERS_MODULE_DIR']
        if module_dir not in sys.path:
            sys.path.insert(0, module_dir)
    
    # If TRANSFORMERS_CACHE is set, create the directory if it doesn't exist
    if 'TRANSFORMERS_CACHE' in env_vars:
        cache_dir = env_vars['TRANSFORMERS_CACHE']
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
    
    # If HF_HOME is set, create the directory if it doesn't exist
    if 'HF_HOME' in env_vars:
        hf_home = env_vars['HF_HOME']
        Path(hf_home).mkdir(parents=True, exist_ok=True)