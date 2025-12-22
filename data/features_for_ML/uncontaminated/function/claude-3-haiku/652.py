import os
import subprocess

def update_submodules(repo_path: str):
    """
    Updates the submodules of the Git repository located at the given path.
    
    Args:
        repo_path (str): The path to the Git repository.
    """
    try:
        # Change the current working directory to the repository path
        os.chdir(repo_path)

        # Initialize the submodules
        subprocess.run(["git", "submodule", "init"], check=True)

        # Update the submodules
        subprocess.run(["git", "submodule", "update", "--remote"], check=True)

    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error updating submodules: {e}")