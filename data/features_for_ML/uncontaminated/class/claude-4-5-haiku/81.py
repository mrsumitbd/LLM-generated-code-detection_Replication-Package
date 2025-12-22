import functools
import subprocess
from typing import Optional, Set


class GitWrapper:

    @functools.lru_cache
    @staticmethod
    def get_closest_tag():
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_repo_version():
        try:
            result = subprocess.run(
                ["git", "describe", "--tags", "--always"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_repo_owner_name():
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                check=True
            )
            url = result.stdout.strip()
            if url.endswith(".git"):
                url = url[:-4]
            if "/" in url:
                return url.split("/")[-2] + "/" + url.split("/")[-1]
            return url
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_repo_remote_name(repo_owner_and_name: str):
        try:
            result = subprocess.run(
                ["git", "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def is_ref_valid(git_ref: str):
        try:
            subprocess.run(
                ["git", "cat-file", "-t", git_ref],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    @functools.lru_cache
    @staticmethod
    def get_remote_branch(local_branch_ref: str, *, repo_owner_and_name: str | None = None):
        try:
            result = subprocess.run(
                ["git", "config", "--get", f"branch.{local_branch_ref}.merge"],
                capture_output=True,
                text=True,
                check=True
            )
            merge_ref = result.stdout.strip()
            if merge_ref.startswith("refs/heads/"):
                return merge_ref[len("refs/heads/"):]
            return merge_ref
        except subprocess.CalledProcessError:
            return local_branch_ref

    @functools.lru_cache
    @staticmethod
    def get_target_remote_branch():
        try:
            current_branch = GitWrapper.get_current_branch()
            result = subprocess.run(
                ["git", "config", "--get", f"branch.{current_branch}.merge"],
                capture_output=True,
                text=True,
                check=True
            )
            merge_ref = result.stdout.strip()
            if merge_ref.startswith("refs/heads/"):
                return merge_ref[len("refs/heads/"):]
            return merge_ref
        except subprocess.CalledProcessError:
            return "main"

    @functools.lru_cache
    @staticmethod
    def get_repo_dir():
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_current_branch():
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def add_files(*files_to_add):
        if not files_to_add:
            return
        try:
            subprocess.run(
                ["git", "add"] + list(files_to_add),
                check=True
            )
        except subprocess.CalledProcessError:
            pass

    @functools.lru_cache
    @staticmethod
    def get_file_add_date(file_path):
        try:
            result = subprocess.run(
                ["git", "log", "--follow", "--format=%aI", "--", file_path],
                capture_output=True,
                text=True,
                check=True
            )
            lines = result.stdout.strip().split("\n")
            if lines:
                return lines[-1]
            return None
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def get_uncommitted_files():
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split("\n")
            return [f for f in files if f]
        except subprocess.CalledProcessError:
            return []

    @staticmethod
    def diff(target_ref: str, base_ref: str, merge_base: bool = False, staged: bool = False):
        try:
            cmd = ["git", "diff"]
            if staged:
                cmd.append("--staged")
            if merge_base:
                merge_base_ref = GitWrapper.merge_base(target_ref, base_ref)
                cmd.extend([merge_base_ref, target_ref])
            else:
                cmd.extend([base_ref, target_ref])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def diff_index(target_ref: str, merge_base: bool = False, staged: bool = False):
        try:
            cmd = ["git", "diff-index"]
            if staged:
                cmd.append("--cached")
            if merge_base:
                merge_base_ref = GitWrapper.merge_base(target_ref, "HEAD")
                cmd.append(merge_base_ref)
            else:
                cmd.append(target_ref)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def merge_base(target_ref: str, base_ref: str = "HEAD"):
        try:
            result = subprocess.run(
                ["git", "merge-base", base_ref, target_ref],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None