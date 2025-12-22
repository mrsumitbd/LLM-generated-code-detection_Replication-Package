import functools

class GitWrapper:

    @functools.lru_cache
    @staticmethod
    def get_closest_tag():
        pass

    @functools.lru_cache
    @staticmethod
    def get_repo_version():
        pass

    @functools.lru_cache
    @staticmethod
    def get_repo_owner_name():
        pass

    @functools.lru_cache
    @staticmethod
    def get_repo_remote_name(repo_owner_and_name: str):
        pass

    @functools.lru_cache
    @staticmethod
    def is_ref_valid(git_ref: str):
        pass

    @functools.lru_cache
    @staticmethod
    def get_remote_branch(local_branch_ref: str, *, repo_owner_and_name: str | None = None):
        pass

    @functools.lru_cache
    @staticmethod
    def get_target_remote_branch():
        pass

    @functools.lru_cache
    @staticmethod
    def get_repo_dir():
        pass

    @functools.lru_cache
    @staticmethod
    def get_current_branch():
        pass

    @staticmethod
    def add_files(*files_to_add):
        pass

    @functools.lru_cache
    @staticmethod
    def get_file_add_date(file_path):
        pass

    @staticmethod
    def get_uncommitted_files():
        pass

    @staticmethod
    def diff(target_ref: str, base_ref: str, merge_base: bool = False, staged: bool = False):
        pass

    @staticmethod
    def diff_index(target_ref: str, merge_base: bool = False, staged: bool = False):
        pass

    @staticmethod
    def merge_base(target_ref: str, base_ref: str = "HEAD"):
        pass