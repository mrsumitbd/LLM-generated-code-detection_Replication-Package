from pathlib import Path
from typing import Optional, List, Set, Any
import re

class PathValidator:
    """Fix for Critical Issue #2: Path Traversal Vulnerability"""

    ALLOWED_DIRS = [
        Path.home() / '.claude',
        Path.home() / '.claude-self-reflect',
        Path.home() / 'projects' / 'claude-self-reflect',
        Path('/tmp')  # For temporary files
    ]

    @staticmethod
    def is_safe_path(path: Path) -> bool:
        """
        Validate that a resolved path is within allowed directories.

        Args:
            path: Path to validate

        Returns:
            True if path is safe, False otherwise
        """
        try:
            resolved = path.expanduser().resolve()

            # Check for path traversal attempts
            if '..' in str(path):
                logger.warning(f"Path traversal attempt detected: {path}")
                return False

            # Check if path is within allowed directories
            for allowed_dir in PathValidator.ALLOWED_DIRS:
                try:
                    resolved.relative_to(allowed_dir.resolve())
                    return True
                except ValueError:
                    continue

            logger.warning(f"Path outside allowed directories: {resolved}")
            return False

        except Exception as e:
            logger.error(f"Path validation error: {e}")
            return False

    @staticmethod
    def sanitize_path(path_str: str) -> Optional[Path]:
        """
        Sanitize and validate a path string.

        Args:
            path_str: Path string to sanitize

        Returns:
            Safe Path object or None if unsafe
        """
        # Remove any null bytes or special characters
        clean_path = re.sub(r'[\x00-\x1f\x7f]', '', path_str)

        path = Path(clean_path)

        if PathValidator.is_safe_path(path):
            return path.expanduser().resolve()

        return None