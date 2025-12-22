def patch_transformers_module_dir(env_vars: dict[str, str]):
    import os

    if 'TRANSFORMERS_OFFLINE' in env_vars and env_vars['TRANSFORMERS_OFFLINE'] == '1':
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
    else:
        os.environ.pop('TRANSFORMERS_OFFLINE', None)