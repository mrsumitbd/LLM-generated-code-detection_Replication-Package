import os
import subprocess
from pathlib import Path
from typing import List


class FallbackRepoManager:
    """
    Utility class for managing a fallback Git repository that contains
    XDC constraint files for various FPGA boards.
    """

    # Default repository location relative to the current working directory
    REPO_DIR = Path.cwd() / "fallback_repo"

    # Default URL for the fallback repository (can be overridden by the
    # environment variable `FALLBACK_REPO_URL`)
    DEFAULT_REPO_URL = "https://github.com/example/fallback-repo.git"

    @staticmethod
    def _repo_url() -> str:
        """Return the repository URL to use."""
        return os.getenv("FALLBACK_REPO_URL", FallbackRepoManager.DEFAULT_REPO_URL)

    @staticmethod
    def ensure_git_repo() -> None:
        """
        Ensure that the fallback repository exists locally. If it does not,
        clone it from the configured URL. If it exists but is not a Git repo,
        raise an exception.
        """
        repo_path = FallbackRepoManager.REPO_DIR
        git_dir = repo_path / ".git"

        if repo_path.exists():
            if not git_dir.exists():
                raise RuntimeError(
                    f"Directory {repo_path} exists but is not a Git repository."
                )
            # Repository already exists; nothing to do
            return

        # Clone the repository
        cmd = ["git", "clone", FallbackRepoManager._repo_url(), str(repo_path)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"Failed to clone repository from {FallbackRepoManager._repo_url()}: "
                f"{exc.stderr.decode().strip()}"
            ) from exc

    @staticmethod
    def _constraints_path(board: str) -> Path:
        """
        Return the path to the constraints directory for a given board.
        """
        return FallbackRepoManager.REPO_DIR / "constraints" / board

    @staticmethod
    def read_xdc_constraints(board: str) -> str:
        """
        Read the primary XDC constraint file for the specified board.
        The file is expected to be named `<board>.xdc` inside the board's
        constraints directory.
        """
        FallbackRepoManager.ensure_git_repo()
        constraints_dir = FallbackRepoManager._constraints_path(board)
        xdc_file = constraints_dir / f"{board}.xdc"

        if not xdc_file.exists():
            raise FileNotFoundError(
                f"Constraint file {xdc_file} does not exist for board '{board}'."
            )

        return xdc_file.read_text(encoding="utf-8")

    @staticmethod
    def read_combined_xdc(board: str) -> str:
        """
        Read and concatenate all XDC files for the specified board.
        All files with the `.xdc` extension inside the board's constraints
        directory are read in sorted order and concatenated with a newline
        separator.
        """
        FallbackRepoManager.ensure_git_repo()
        constraints_dir = FallbackRepoManager._constraints_path(board)

        if not constraints_dir.exists():
            raise FileNotFoundError(
                f"Constraints directory {constraints_dir} does not exist for board '{board}'."
            )

        xdc_files: List[Path] = sorted(constraints_dir.glob("*.xdc"))
        if not xdc_files:
            raise FileNotFoundError(
                f"No XDC files found in {constraints_dir} for board '{board}'."
            )

        contents = []
        for xdc_file in xdc_files:
            contents.append(xdc_file.read_text(encoding="utf-8"))

        return "\n".join(contents)