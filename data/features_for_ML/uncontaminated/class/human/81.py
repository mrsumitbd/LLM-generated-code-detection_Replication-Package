import functools
import datetime
import os
import re
import subprocess

class GitWrapper:

    @functools.lru_cache
    @staticmethod
    def get_closest_tag():
        """
        Determines the version of the repo by using `git describe`

        Returns
        -------
        str
            The full version of the repo in the format 'v#.#.#{a|b|rc}'
        """
        return _git("describe", "--first-parent", "--tags", "--abbrev=0")

    @functools.lru_cache
    @staticmethod
    def get_repo_version():
        """
        Determines the version of the repo using `git describe` and returns only
        the major and minor portion

        Returns
        -------
        str
            The partial version of the repo in the format '{major}.{minor}'
        """

        full_repo_version = GitWrapper.get_closest_tag()

        match = re.match(r"^v?(?P<major>[0-9]+)(?:\.(?P<minor>[0-9]+))?", full_repo_version)

        if (match is None):
            logger.debug("Could not determine repo major minor version. Full repo version: %s.", full_repo_version)
            return None

        out_version = match.group("major")

        if (match.group("minor")):
            out_version += "." + match.group("minor")

        return out_version

    @functools.lru_cache
    @staticmethod
    def get_repo_owner_name():

        return "NVIDIA/" + _run_cmd("git remote -v | grep -oP '/\\K\\w*(?=\\.git \\(fetch\\))' | head -1")

    @functools.lru_cache
    @staticmethod
    def get_repo_remote_name(repo_owner_and_name: str):

        return _run_cmd(f"git remote -v | grep :{repo_owner_and_name} | grep \"(fetch)\" | head -1 | cut -f1")

    @functools.lru_cache
    @staticmethod
    def is_ref_valid(git_ref: str):

        try:
            return _git("rev-parse", "--verify", git_ref) != ""
        except subprocess.CalledProcessError:
            return False

    @functools.lru_cache
    @staticmethod
    def get_remote_branch(local_branch_ref: str, *, repo_owner_and_name: str | None = None):

        if (repo_owner_and_name is None):
            repo_owner_and_name = GitWrapper.get_repo_owner_name()

        remote_name = GitWrapper.get_repo_remote_name(repo_owner_and_name)

        remote_branch_ref = f"{remote_name}/{local_branch_ref}"

        if (GitWrapper.is_ref_valid(remote_branch_ref)):
            return remote_branch_ref

        logger.info("Remote branch '%s' for repo '%s' does not exist. Falling back to rev-parse",
                    remote_branch_ref,
                    repo_owner_and_name)

        remote_branch_ref = _git("rev-parse", "--abbrev-ref", "--symbolic-full-name", local_branch_ref + "@{upstream}")

        return remote_branch_ref

    @functools.lru_cache
    @staticmethod
    def get_target_remote_branch():
        base_ref = os.environ.get("CI_MERGE_REQUEST_TARGET_BRANCH_NAME")
        if (base_ref is not None):
            return base_ref

        try:
            base_ref = "develop"

            # If our current branch and the base ref are the same, then use main
            if (base_ref == GitWrapper.get_current_branch()):
                logger.warning("Current branch is the same as the tagged branch: %s. Falling back to 'main'", base_ref)
                base_ref = "develop"

        except Exception:
            logger.exception("Could not determine branch version falling back to develop", exc_info=True)
            base_ref = "develop"

        return GitWrapper.get_remote_branch(base_ref)

    @functools.lru_cache
    @staticmethod
    def get_repo_dir():
        """
        Returns the top level directory for this git repo
        """
        return _git("rev-parse", "--show-toplevel")

    @functools.lru_cache
    @staticmethod
    def get_current_branch():
        """Returns the name of the current branch"""
        name = _git("rev-parse", "--abbrev-ref", "HEAD")
        name = name.rstrip()
        return name

    @staticmethod
    def add_files(*files_to_add):
        """Runs git add on file"""
        return _git("add", *files_to_add)

    @functools.lru_cache
    @staticmethod
    def get_file_add_date(file_path):
        """Return the date a given file was added to git"""
        date_str = _run_cmd(f"git log --follow --format=%as -- {file_path} | tail -n 1")
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")

    @staticmethod
    def get_uncommitted_files():
        """
        Returns a list of all changed files that are not yet committed. This
        means both untracked/unstaged as well as uncommitted files too.
        """
        files = _git("status", "-u", "-s")
        ret = []
        for f in files.splitlines():
            f = f.strip(" ")
            f = re.sub(r"\s+", " ", f)  # noqa: W605
            tmp = f.split(" ", 1)
            # only consider staged files or uncommitted files
            # in other words, ignore untracked files
            if tmp[0] == "M" or tmp[0] == "A":
                ret.append(tmp[1])
        return ret

    @staticmethod
    def diff(target_ref: str, base_ref: str, merge_base: bool = False, staged: bool = False):

        assert base_ref is not None or base_ref != "", "base_ref must be a valid ref"
        assert target_ref is not None or target_ref != "", "target_ref must be a valid ref"

        args = ["--no-pager", "diff", "--name-only", "--ignore-submodules"]

        if (merge_base):
            args.append("--merge-base")

        if (staged):
            args.append("--cached")

        args += [target_ref, base_ref]

        return _git(*args).splitlines()

    @staticmethod
    def diff_index(target_ref: str, merge_base: bool = False, staged: bool = False):

        assert target_ref is not None or target_ref != "", "target_ref must be a valid ref"

        args = ["--no-pager", "diff-index", "--name-only", "--ignore-submodules"]

        if (merge_base):
            args.append("--merge-base")

        if (staged):
            args.append("--cached")

        args += [target_ref]

        return _git(*args).splitlines()

    @staticmethod
    def merge_base(target_ref: str, base_ref: str = "HEAD"):

        assert base_ref is not None or base_ref != "", "base_ref must be a valid ref"
        assert target_ref is not None or target_ref != "", "target_ref must be a valid ref"

        return _git("merge-base", target_ref, base_ref)