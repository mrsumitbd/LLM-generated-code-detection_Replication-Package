import os
import subprocess
from typing import Optional

class BranchManager:
    """Manages versions across main and mcp-remote branches safely."""

    def __init__(self):
        self.current_branch = self.get_current_branch()
        self.version = self.get_version_from_pyproject()

    def get_current_branch(self) -> str:
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()

    def get_version_from_pyproject(self) -> str:
        with open('pyproject.toml', 'r') as file:
            for line in file:
                if line.startswith('version = '):
                    return line.split('=')[1].strip().strip('"')
        return ''

    def show_status(self):
        print(f'Current branch: {self.current_branch}')
        print(f'Current version: {self.version}')

    def bump_version(self, new_version: str):
        with open('pyproject.toml', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.startswith('version = '):
                lines[i] = f'version = "{new_version}"\n'
                break

        with open('pyproject.toml', 'w') as file:
            file.writelines(lines)

        self.version = new_version

    def create_version_tag(self, version: Optional[str] = None):
        if version is None:
            version = self.version
        subprocess.run(['git', 'tag', version])

    def save_state(self):
        subprocess.run(['git', 'add', 'pyproject.toml'])
        subprocess.run(['git', 'commit', '-m', f'Bump version to {self.version}'])
        subprocess.run(['git', 'push'])
        self.create_version_tag()