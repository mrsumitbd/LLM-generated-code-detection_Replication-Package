def _cpp_extention_load_helper(name, sources, extra_cuda_flags):
    import os
    import subprocess
    import tempfile
    import shutil
    from pathlib import Path
    
    # Create a temporary directory for building
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Copy source files to temp directory
        source_files = []
        for source in sources:
            src_path = Path(source)
            if src_path.exists():
                dst_path = tmpdir / src_path.name
                shutil.copy2(src_path, dst_path)
                source_files.append(str(dst_path))
        
        # Create a setup.py file for building the extension
        setup_content = f"""
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools

class build_ext_custom(build_ext):
    def build_extensions(self):
        super().build_extensions()

ext_modules = [
    Extension(
        '{name}',
        {source_files},
        extra_compile_args=['-O3'],
        extra_link_args=[],
    ),
]

setup(
    name='{name}',
    ext_modules=ext_modules,
    cmdclass={{'build_ext': build_ext_custom}},
)
"""
        
        setup_file = tmpdir / "setup.py"
        setup_file.write_text(setup_content)
        
        # Build the extension
        build_dir = tmpdir / "build"
        build_dir.mkdir(exist_ok=True)
        
        cmd = [
            sys.executable,
            str(setup_file),
            "build_ext",
            "--inplace",
            f"--build-temp={build_dir}",
        ]
        
        if extra_cuda_flags:
            cmd.extend(extra_cuda_flags)
        
        result = subprocess.run(cmd, cwd=str(tmpdir), capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Failed to build extension: {result.stderr}")
        
        # Find and return the built extension
        import glob
        so_files = glob.glob(str(tmpdir / f"{name}*.so")) + glob.glob(str(tmpdir / f"{name}*.pyd"))
        
        if so_files:
            return so_files[0]
        
        return None