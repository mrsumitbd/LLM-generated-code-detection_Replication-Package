from codegen.cli.env.enums import Environment
from codegen.cli.env.global_env import global_env

def get_modal_prefix():
    workspace = get_modal_workspace()
    if global_env.ENV == Environment.DEVELOP and global_env.MODAL_ENVIRONMENT:
        return f"{workspace}-{global_env.MODAL_ENVIRONMENT}"
    return workspace