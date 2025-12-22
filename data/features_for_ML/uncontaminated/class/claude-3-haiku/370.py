import os
import pathlib

class FilesystemSandbox:
    """Filesystem sandbox that restricts file operations to a safe directory."""

    def __init__(self, root_path: str | None = None):
        if root_path is None:
            self.root_path = os.path.join(os.path.expanduser("~"), ".sandbox")
        else:
            self.root_path = root_path
        self.ensure_safe_directory()

    def ensure_safe_directory(self):
        pathlib.Path(self.root_path).mkdir(parents=True, exist_ok=True)

    def is_path_safe(self, path: str) -> bool:
        try:
            real_path = os.path.realpath(os.path.join(self.root_path, path))
            return real_path.startswith(os.path.realpath(self.root_path))
        except (ValueError, OSError):
            return False

    def sanitize_path(self, path: str) -> str:
        return os.path.normpath(path.strip("/"))

    def create_safe_path(self, filename: str) -> str:
        sanitized_filename = self.sanitize_path(filename)
        return os.path.join(self.root_path, sanitized_filename)

    def get_sandbox_root(self) -> str:
        return self.root_path

    def cleanup(self):
        try:
            for root, dirs, files in os.walk(self.root_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            os.rmdir(self.root_path)
        except OSError:
            pass