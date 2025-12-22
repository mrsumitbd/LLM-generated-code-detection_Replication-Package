import os
import subprocess
import shutil

class FallbackRepoManager:
    REPO_DIR = "xdc_repo"
    REPO_URL = "https://example.com/xdc_repo.git"

    @staticmethod
    def read_xdc_constraints(board: str) -> str:
        FallbackRepoManager.ensure_git_repo()
        file_path = os.path.join(FallbackRepoManager.REPO_DIR, f"{board}.xdc")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        else:
            return ""

    @staticmethod
    def read_combined_xdc(board: str) -> str:
        FallbackRepoManager.ensure_git_repo()
        file_path = os.path.join(FallbackRepoManager.REPO_DIR, "combined.xdc")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        else:
            return ""

    @staticmethod
    def ensure_git_repo():
        if not os.path.exists(FallbackRepoManager.REPO_DIR):
            subprocess.run(["git", "clone", FallbackRepoManager.REPO_URL, FallbackRepoManager.REPO_DIR], check=True)
        else:
            subprocess.run(["git", "-C", FallbackRepoManager.REPO_DIR, "pull"], check=True)