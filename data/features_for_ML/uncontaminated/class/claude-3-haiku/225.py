import os
from pathlib import Path
from typing import Optional

class PathValidator:
    """Fix for Critical Issue #2: Path Traversal Vulnerability"""

    @staticmethod
    def is_safe_path(path: Path) -> bool:
        try:
            real_path = path.resolve(strict=True)
            return str(real_path).startswith(str(path.root))
        except (FileNotFoundError, ValueError):
            return False

    @staticmethod
    def sanitize_path(path_str: str) -> Optional[Path]:
        try:
            path = Path(path_str).resolve(strict=True)
            if PathValidator.is_safe_path(path):
                return path
            else:
                return None
        except (FileNotFoundError, ValueError):
            return None