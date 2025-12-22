def check_if_cuda_home_none(global_option: str) -> None:
    import os
    import sys
    
    cuda_home = os.environ.get('CUDA_HOME')
    
    if cuda_home is None:
        raise RuntimeError(
            f"CUDA_HOME environment variable is not set. "
            f"Please set CUDA_HOME to the directory where CUDA is installed, "
            f"or use the --{global_option} option to specify the CUDA installation path."
        )