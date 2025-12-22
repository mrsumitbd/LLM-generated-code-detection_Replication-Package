import os
import shutil

class FilesystemSandbox:
    """Filesystem sandbox that restricts file operations to a safe directory."""

    def __init__(self, root_path: str | None = None):
        self.root_path = root_path or os.path.join(os.getcwd(), 'sandbox')

    def ensure_safe_directory(self):
        os.makedirs(self.root_path, exist_ok=True)

    def is_path_safe(self, path: str) -> bool:
        return os.path.commonpath([os.path.abspath(path), os.path.abspath(self.root_path)]) == os.path.abspath(self.root_path)

    def sanitize_path(self, path: str) -> str:
        return os.path.abspath(os.path.join(self.root_path, os.path.relpath(path, '/')))

    def create_safe_path(self, filename: str) -> str:
        return os.path.join(self.root_path, filename)

    def get_sandbox_root(self) -> str:
        return self.root_path

    def cleanup(self):
        shutil.rmtree(self.root_path)