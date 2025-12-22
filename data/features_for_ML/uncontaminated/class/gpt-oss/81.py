import functools
import subprocess
import os
from pathlib import Path
from typing import List, Optional


class GitWrapper:
    @functools.lru_cache
    @staticmethod
    def _run_git(args: List[str], cwd: Optional[Path] = None, capture_output: bool = True) -> str:
        """Run a git command and return its stdout as a string."""
        if cwd is None:
            cwd = GitWrapper.get_repo_dir()
        result = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            text=True,
            capture_output=capture_output,
            check=True,
        )
        return result.stdout.strip()

    @functools.lru_cache
    @staticmethod
    def get_closest_tag() -> str:
        """Return the most recent tag reachable from HEAD."""
        return GitWrapper._run_git(["describe", "--tags", "--abbrev=0"])

    @functools.lru_cache
    @staticmethod
    def get_repo_version() -> str:
        """Return a human‑readable version string for the current commit."""
        return GitWrapper._run_git(["describe", "--tags", "--always", "--dirty"])

    @functools.lru_cache
    @staticmethod
    def get_repo_owner_name() -> str:
        """Return the GitHub owner name extracted from the origin remote URL."""
        url = GitWrapper._run_git(["remote", "get-url", "origin"])
        # Handle https://github.com/owner/repo.git or git@github.com:owner/repo.git
        if url.startswith("git@"):
            path = url.split(":", 1)[1]
        else:
            path = url.split("://", 1)[1]
        owner, _ = path.split("/", 1)
        return owner

    @functools.lru_cache
    @staticmethod
    def get_repo_remote_name(repo_owner_and_name: str) -> str:
        """Return the remote name that points to the given owner/repo."""
        remotes = GitWrapper._run_git(["remote"]).splitlines()
        for remote in remotes:
            url = GitWrapper._run_git(["remote", "get-url", remote])
            if repo_owner_and_name in url:
                return remote
        raise ValueError(f"No remote found for {repo_owner_and_name}")

    @functools.lru_cache
    @staticmethod
    def is_ref_valid(git_ref: str) -> bool:
        """Return True if the given ref exists in the repository."""
        try:
            GitWrapper._run_git(["rev-parse", "--verify", git_ref])
            return True
        except subprocess.CalledProcessError:
            return False

    @functools.lru_cache
    @staticmethod
    def get_remote_branch(local_branch_ref: str, *, repo_owner_and_name: Optional[str] = None) -> str:
        """Return the remote branch name that the local branch tracks."""
        if repo_owner_and_name is None:
            repo_owner_and_name = f"{GitWrapper.get_repo_owner_name()}/{Path(GitWrapper.get_repo_dir()).name}"
        remote = GitWrapper.get_repo_remote_name(repo_owner_and_name)
        # Use symbolic-ref to get upstream
        try:
            upstream = GitWrapper._run_git(
                ["rev-parse", "--abbrev-ref", "--symbolic-full-name", f"{local_branch_ref}@{{upstream}}"]
            )
            return upstream.split("/", 1)[1]  # return branch part
        except subprocess.CalledProcessError:
            raise ValueError(f"Branch {local_branch_ref} does not track a remote branch")

    @functools.lru_cache
    @staticmethod
    def get_target_remote_branch() -> str:
        """Return the remote branch that the current branch tracks."""
        current = GitWrapper.get_current_branch()
        return GitWrapper.get_remote_branch(current)

    @functools.lru_cache
    @staticmethod
    def get_repo_dir() -> Path:
        """Return the absolute path to the repository root."""
        return Path(GitWrapper._run_git(["rev-parse", "--show-toplevel"]))

    @functools.lru_cache
    @staticmethod
    def get_current_branch() -> str:
        """Return the name of the current branch."""
        return GitWrapper._run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    @staticmethod
    def add_files(*files_to_add: str) -> None:
        """Stage the given files for commit."""
        if files_to_add:
            subprocess.run(["git", "add"] + list(files_to_add), check=True)

    @functools.lru_cache
    @staticmethod
    def get_file_add_date(file_path: str) -> int:
        """Return the commit timestamp when the file was first added."""
        return int(
            GitWrapper._run_git(
                ["log", "--diff-filter=A", "--follow", "--format=%ct", "--", file_path]
            ).splitlines()[-1]
        )

    @staticmethod
    def get_uncommitted_files() -> List[str]:
        """Return a list of uncommitted (modified or untracked) files."""
        status = GitWrapper._run_git(["status", "--porcelain"])
        files = []
        for line in status.splitlines():
            if line:
                # first two chars are status, rest is file path
                files.append(line[3:].strip())
        return files

    @staticmethod
    def diff(target_ref: str, base_ref: str, merge_base: bool = False, staged: bool = False) -> str:
        """Return the diff between two refs."""
        args = ["diff"]
        if merge_base:
            args.append("--merge-base")
        if staged:
            args.append("--staged")
        args += [target_ref, base_ref]
        return GitWrapper._run_git(args)

    @staticmethod
    def diff_index(target_ref: str, merge_base: bool = False, staged: bool = False) -> str:
        """Return the diff-index between a ref and the index."""
        args = ["diff-index"]
        if merge_base:
            args.append("--merge-base")
        if staged:
            args.append("--staged")
        args += [target_ref]
        return GitWrapper._run_git(args)

    @staticmethod
    def merge_base(target_ref: str, base_ref: str = "HEAD") -> str:
        """Return the merge base commit hash between two refs."""
        return GitWrapper._run_git(["merge-base", target_ref, base_ref])