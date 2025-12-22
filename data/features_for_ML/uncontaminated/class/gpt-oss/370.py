import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional


class FilesystemSandbox:
    """Filesystem sandbox that restricts file operations to a safe directory."""

    def __init__(self, root_path: str | None = None):
        """
        Initialize the sandbox.

        :param root_path: Optional path to the sandbox root. If None, a temporary
                          directory will be created.
        """
        self._temp_root: bool = False
        if root_path is None:
            self._root = Path(tempfile.mkdtemp(prefix="sandbox_"))
            self._temp_root = True
        else:
            self._root = Path(root_path).expanduser().resolve()
        self.ensure_safe_directory()

    def ensure_safe_directory(self):
        """Create the sandbox root directory if it does not exist."""
        if not self._root.exists():
            self._root.mkdir(parents=True, exist_ok=True)
        if not self._root.is_dir():
            raise NotADirectoryError(f"Sandbox root {self._root} is not a directory")

    def is_path_safe(self, path: str) -> bool:
        """
        Check whether a given path is inside the sandbox.

        :param path: Path to check.
        :return: True if the path is within the sandbox, False otherwise.
        """
        try:
            resolved = Path(path).expanduser().resolve(strict=False)
        except Exception:
            return False
        try:
            resolved.relative_to(self._root)
            return True
        except ValueError:
            return False

    def sanitize_path(self, path: str) -> str:
        """
        Sanitize a path by removing absolute components and normalizing it.

        :param path: Path to sanitize.
        :return: Sanitized relative path string.
        """
        # Remove leading slashes and normalize
        p = Path(path).expanduser()
        parts = [part for part in p.parts if part not in ("", ".", "..")]
        sanitized = Path(*parts)
        return str(sanitized)

    def create_safe_path(self, filename: str) -> str:
        """
        Create a safe absolute path inside the sandbox for a given filename.

        :param filename: Filename or relative path.
        :return: Absolute path inside the sandbox.
        """
        sanitized = self.sanitize_path(filename)
        safe_path = self._root / sanitized
        # Ensure the resulting path is still inside the sandbox
        if not self.is_path_safe(str(safe_path)):
            raise ValueError(f"Path {filename} resolves outside the sandbox")
        # Create parent directories if needed
        safe_path.parent.mkdir(parents=True, exist_ok=True)
        return str(safe_path)

    def get_sandbox_root(self) -> str:
        """Return the absolute path of the sandbox root."""
        return str(self._root)

    def cleanup(self):
        """Remove the sandbox directory if it was created as a temporary directory."""
        if self._temp_root and self._root.exists():
            shutil.rmtree(self._root, ignore_errors=True)
        self._root = None