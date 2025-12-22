def _cpp_extention_load_helper(name, sources, extra_cuda_flags):
    import torch
    from setuptools import setup
    from torch.utils.cpp_extension import BuildExtension, CUDAExtension

    setup(
        name=name,
        ext_modules=[
            CUDAExtension(
                name=name,
                sources=sources,
                extra_compile_args={'cxx': ['-g'],
                                    'nvcc': extra_cuda_flags}
            )
        ],
        cmdclass={
            'build_ext': BuildExtension
        }
    )