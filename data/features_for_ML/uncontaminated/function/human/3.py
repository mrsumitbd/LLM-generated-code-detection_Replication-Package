from typing import List, Literal, Optional, Tuple
from fenic._backends.local.utils.io_utils import PathScheme, get_path_scheme

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

        path_scheme = get_path_scheme(paths[0])
        if path_scheme == PathScheme.S3:
            return DocFolderLoader._enumerate_files_s3(paths, valid_file_extension, exclude_pattern, recursive)
        elif path_scheme == PathScheme.HF:
            return DocFolderLoader._enumerate_files_hf(paths, valid_file_extension, exclude_pattern, recursive)
        else:
            return DocFolderLoader._enumerate_files_local_fs(paths, valid_file_extension, exclude_pattern, recursive)