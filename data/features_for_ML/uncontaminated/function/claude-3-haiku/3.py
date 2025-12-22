import os
import re
from typing import List, Optional

def _enumerate_files(
        paths: list[str],
        valid_file_extension: str,
        exclude_pattern: Optional[str] = None,
        recursive: bool = False
    ) -> List[str]:
        r"""Enumerate files in a folder based on include and exclude patterns.

        Args:
            paths: paths to the folders to traverse, these will be glob patterns.
            exclude_pattern: Regex pattern to exclude files (e.g., r"\.tmp$", r"temp.*")
            recursive: Whether to traverse subdirectories recursively

        Returns:
            List of Path objects for matching files
        """
        files = []
        for path in paths:
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith(valid_file_extension):
                        file_path = os.path.join(root, filename)
                        if exclude_pattern:
                            if not re.search(exclude_pattern, file_path):
                                files.append(file_path)
                        else:
                            files.append(file_path)
                if not recursive:
                    break
        return files