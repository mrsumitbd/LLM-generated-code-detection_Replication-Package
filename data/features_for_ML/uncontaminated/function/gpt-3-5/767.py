def check_if_cuda_home_none(global_option: str) -> None:
    if global_option == 'CUDA_HOME':
        if os.environ.get('CUDA_HOME') is None:
            print('CUDA_HOME is not set.')
        else:
            print('CUDA_HOME is set.')
    else:
        print('Invalid global option provided.')