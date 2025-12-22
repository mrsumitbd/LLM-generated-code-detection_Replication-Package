import os
import sys
import subprocess
import shutil
import tempfile
from setuptools import Extension
from setuptools.command.build_ext import build_ext

def _cpp_extention_load_helper(name, sources, extra_cuda_flags):
    class CustomBuildExt(build_ext):
        def build_extension(self, ext):
            try:
                self.compiler.compiler_so
            except AttributeError:
                self.compiler.compiler_so = self.compiler.compiler
            super().build_extension(ext)

    ext = Extension(name, sources=sources)
    ext.extra_compile_args = ['-std=c++11']
    ext.extra_link_args = ['-std=c++11']

    if sys.platform == 'darwin':
        ext.extra_compile_args += ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        ext.extra_link_args += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

    if extra_cuda_flags:
        ext.extra_compile_args += extra_cuda_flags
        ext.extra_link_args += extra_cuda_flags

    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            subprocess.check_call([sys.executable, 'setup.py', 'build_ext', '--inplace'], cwd=tmp_dir)
            shutil.copy(os.path.join(tmp_dir, f'{name}.so'), os.path.join(os.path.dirname(__file__), f'{name}.so'))
        except subprocess.CalledProcessError as e:
            print(f'Error building C++ extension: {e}')
            return None

    return ext