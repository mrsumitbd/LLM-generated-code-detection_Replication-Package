import os
import torch
from torch.utils.cpp_extension import load

def _cpp_extention_load_helper(name, sources, extra_cuda_flags):
    """
    Helper to compile and load a C++/CUDA extension.

    Parameters
    ----------
    name : str
        Name of the extension module.
    sources : list[str]
        List of source file paths (C++, CUDA, etc.).
    extra_cuda_flags : list[str] | None
        Extra compiler flags for the CUDA compiler.

    Returns
    -------
    module
        The loaded extension module.
    """
    # Ensure sources are absolute paths
    abs_sources = [os.path.abspath(src) for src in sources]

    # Determine if CUDA is available
    cuda_available = torch.cuda.is_available()

    # Build arguments
    kwargs = {
        "name": name,
        "sources": abs_sources,
        "verbose": True,
    }

    if cuda_available:
        # Pass CUDA flags if provided
        if extra_cuda_flags:
            kwargs["extra_cuda_cflags"] = extra_cuda_flags
    else:
        # If CUDA is not available, ignore CUDA flags
        pass

    # Load the extension
    return load(**kwargs)