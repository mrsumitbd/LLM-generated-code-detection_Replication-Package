import os
import subprocess
from pathlib import Path
from typing import Tuple

def update_submodules(repo_path: str) -> Tuple[int, str, str]:
    """
    Update all git submodules in the repository located at `repo_path`.

    Parameters
    ----------
    repo_path : str
        Path to the root of the git repository.

    Returns
    -------
    Tuple[int, str, str]
        A tuple containing the return code, stdout, and stderr of the
        git command.

    Raises
    ------
    FileNotFoundError
        If the specified repository path does not exist.
    RuntimeError
        If the git command fails (non-zero return code).
    """
    repo = Path(repo_path).expanduser().resolve()
    if not repo.is_dir():
        raise FileNotFoundError(f"Repository path does not exist: {repo}")

    # Ensure we are inside a git repository
    git_dir = repo / ".git"
    if not git_dir.is_dir():
        raise RuntimeError(f"Not a git repository: {repo}")

    # Prepare the git submodule update command
    cmd = ["git", "submodule", "update", "--init", "--recursive"]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(repo),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("git executable not found") from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"git submodule update failed with return code {result.returncode}\n"
            f"stdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    return result.returncode, result.stdout, result.stderr