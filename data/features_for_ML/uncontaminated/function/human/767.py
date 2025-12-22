from torch.utils.cpp_extension import CUDA_HOME, BuildExtension, CUDAExtension
import warnings

def check_if_cuda_home_none(global_option: str) -> None:
    if CUDA_HOME is not None:
        return
    # Warn instead of error: users may be downloading prebuilt wheels; nvcc not required in that case.
    warnings.warn(
        f"{global_option} was requested, but nvcc was not found.  Are you sure your environment has nvcc available?  "
        "If you're installing within a container from https://hub.docker.com/r/pytorch/pytorch, "
        "only images whose names contain 'devel' will provide nvcc."
    )