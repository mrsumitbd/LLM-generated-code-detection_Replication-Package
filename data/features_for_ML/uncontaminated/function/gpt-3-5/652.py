import subprocess

def update_submodules(repo_path: str):
    subprocess.run(['git', 'submodule', 'update', '--init', '--recursive'], cwd=repo_path)