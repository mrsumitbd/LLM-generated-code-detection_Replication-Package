import functools
import subprocess
import os
from typing import List, Tuple, Optional

class GitWrapper:

    @functools.lru_cache
    @staticmethod
    def get_closest_tag() -> str:
        try:
            return subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
        except subprocess.CalledProcessError:
            return ''

    @functools.lru_cache
    @staticmethod
    def get_repo_version() -> str:
        try:
            return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
        except subprocess.CalledProcessError:
            return ''

    @functools.lru_cache
    @staticmethod
    def get_repo_owner_name() -> str:
        try:
            return subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).decode().strip().split('/')[-2]
        except subprocess.CalledProcessError:
            return ''

    @functools.lru_cache
    @staticmethod
    def get_repo_remote_name(repo_owner_and_name: str) -> str:
        try:
            return subprocess.check_output(['git', 'config', '--get', f'remote.{repo_owner_and_name}.url']).decode().strip()
        except subprocess.CalledProcessError:
            return ''

    @functools.lru_cache
    @staticmethod
    def is_ref_valid(git_ref: str) -> bool:
        try:
            subprocess.check_output(['git', 'show-ref', '--verify', '--quiet', git_ref])
            return True
        except subprocess.CalledProcessError:
            return False

    @functools.lru_cache
    @staticmethod
    def get_remote_branch(local_branch_ref: str, *, repo_owner_and_name: str | None = None) -> Optional[str]:
        try:
            if repo_owner_and_name:
                remote_name = GitWrapper.get_repo_remote_name(repo_owner_and_name)
            else:
                remote_name = 'origin'
            return subprocess.check_output(['git', 'show-ref', '--verify', '--quiet', f'refs/remotes/{remote_name}/{local_branch_ref}']).decode().strip().split()[1]
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_target_remote_branch() -> Optional[str]:
        try:
            return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']).decode().strip()
        except subprocess.CalledProcessError:
            return None

    @functools.lru_cache
    @staticmethod
    def get_repo_dir() -> str:
        try:
            return subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode().strip()
        except subprocess.CalledProcessError:
            return ''

    @functools.lru_cache
    @staticmethod
    def get_current_branch() -> str:
        try:
            return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        except subprocess.CalledProcessError:
            return ''

    @staticmethod
    def add_files(*files_to_add: str) -> None:
        subprocess.run(['git', 'add'] + list(files_to_add), check=True)

    @functools.lru_cache
    @staticmethod
    def get_file_add_date(file_path: str) -> str:
        try:
            return subprocess.check_output(['git', 'log', '--format=%ai', '--', file_path]).decode().strip().split('\n')[-1]
        except subprocess.CalledProcessError:
            return ''

    @staticmethod
    def get_uncommitted_files() -> List[str]:
        try:
            output = subprocess.check_output(['git', 'status', '--porcelain']).decode().strip()
            return [line.split()[1] for line in output.split('\n')]
        except subprocess.CalledProcessError:
            return []

    @staticmethod
    def diff(target_ref: str, base_ref: str, merge_base: bool = False, staged: bool = False) -> Tuple[str, str]:
        cmd = ['git', 'diff']
        if merge_base:
            cmd.append(f'{base_ref}...{target_ref}')
        else:
            cmd.append(f'{base_ref} {target_ref}')
        if staged:
            cmd.append('--staged')
        try:
            stdout = subprocess.check_output(cmd).decode().strip()
            stderr = ''
        except subprocess.CalledProcessError as e:
            stdout = ''
            stderr = e.stderr.decode().strip()
        return stdout, stderr

    @staticmethod
    def diff_index(target_ref: str, merge_base: bool = False, staged: bool = False) -> Tuple[str, str]:
        cmd = ['git', 'diff-index']
        if merge_base:
            cmd.append(f'{target_ref}')
        else:
            cmd.append(f'{target_ref} --')
        if staged:
            cmd.append('--cached')
        try:
            stdout = subprocess.check_output(cmd).decode().strip()
            stderr = ''
        except subprocess.CalledProcessError as e:
            stdout = ''
            stderr = e.stderr.decode().strip()
        return stdout, stderr

    @staticmethod
    def merge_base(target_ref: str, base_ref: str = "HEAD") -> str:
        try:
            return subprocess.check_output(['git', 'merge-base', target_ref, base_ref]).decode().strip()
        except subprocess.CalledProcessError:
            return ''