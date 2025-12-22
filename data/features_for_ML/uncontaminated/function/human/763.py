import subprocess
import os

def _no_need_subversion():
    try:
        modified_files = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stderr=subprocess.DEVNULL
        ).decode().splitlines()
        
        current_file = os.path.relpath(__file__, os.getcwd())
        
        # If this file is modified, indicating the main version is updated
        if current_file in modified_files:
            return True
        
        # If codes in the abacustest directory are modified, indicating the main version is not updated
        for i in modified_files:
            if i.startswith("abacustest/"):
                return False
        
        return True
    except:
        return False