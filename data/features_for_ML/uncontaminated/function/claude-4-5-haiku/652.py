import subprocess
import os

def update_submodules(repo_path: str):
    """Update all submodules in a git repository."""
    # Change to the repository directory
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        
        # Initialize and update all submodules
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            check=True,
            capture_output=True,
            text=True
        )
    finally:
        # Change back to the original directory
        os.chdir(original_dir)