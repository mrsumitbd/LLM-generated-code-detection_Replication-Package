def check_if_cuda_home_none(global_option: str) -> None:
    import os

    cuda_home = os.environ.get('CUDA_HOME', None)
    if cuda_home is None:
        if global_option == 'train':
            raise ValueError('CUDA_HOME environment variable is not set. Please set it to the appropriate CUDA installation directory.')
        else:
            print('CUDA_HOME environment variable is not set. Defaulting to CPU-only mode.')