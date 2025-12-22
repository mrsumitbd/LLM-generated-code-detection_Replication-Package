import os
import tempfile
import shutil
from pathlib import Path


class FilesystemSandbox:
    """Filesystem sandbox that restricts file operations to a safe directory."""

    def __init__(self, root_path: str | None = None):
        if root_path is None:
            self.root_path = tempfile.mkdtemp(prefix="sandbox_")
        else:
            self.root_path = os.path.abspath(root_path)
        self.ensure_safe_directory()

    def ensure_safe_directory(self):
        """Ensure the sandbox root directory exists."""
        os.makedirs(self.root_path, exist_ok=True)

    def is_path_safe(self, path: str) -> bool:
        """Check if a path is within the sandbox root directory."""
        try:
            abs_path = os.path.abspath(os.path.join(self.root_path, path))
            real_root = os.path.realpath(self.root_path)
            real_path = os.path.realpath(abs_path)
            return real_path.startswith(real_root + os.sep) or real_path == real_root
        except (OSError, ValueError):
            return False

    def sanitize_path(self, path: str) -> str:
        """Sanitize a path by removing dangerous components."""
        # Remove leading slashes and null bytes
        path = path.lstrip(os.sep).replace('\0', '')
        # Remove parent directory references
        path = path.replace('..', '')
        # Normalize the path
        path = os.path.normpath(path)
        return path

    def create_safe_path(self, filename: str) -> str:
        """Create a safe absolute path within the sandbox."""
        sanitized = self.sanitize_path(filename)
        safe_path = os.path.join(self.root_path, sanitized)
        
        if not self.is_path_safe(safe_path):
            raise ValueError(f"Path '{filename}' is outside sandbox boundaries")
        
        return safe_path

    def get_sandbox_root(self) -> str:
        """Get the root directory of the sandbox."""
        return self.root_path

    def cleanup(self):
        """Clean up the sandbox directory."""
        if os.path.exists(self.root_path):
            shutil.rmtree(self.root_path)