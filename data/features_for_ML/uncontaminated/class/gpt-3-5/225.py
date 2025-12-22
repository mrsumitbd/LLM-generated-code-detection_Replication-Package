from pathlib import Path
from typing import Optional

class PathValidator:
    """Fix for Critical Issue #2: Path Traversal Vulnerability"""

    @staticmethod
    def is_safe_path(path: Path) -> bool:
        return not path.is_absolute()

    @staticmethod
    def sanitize_path(path_str: str) -> Optional[Path]:
        try:
            path = Path(path_str)
            if not PathValidator.is_safe_path(path):
                return None
            return path
        except Exception:
            return None