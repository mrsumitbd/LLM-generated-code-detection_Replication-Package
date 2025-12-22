import subprocess
import json
import os
from pathlib import Path
from typing import Optional
import toml


class BranchManager:
    """Manages versions across main and mcp-remote branches safely."""

    def __init__(self):
        self.repo_root = self._find_repo_root()
        self.pyproject_path = self.repo_root / "pyproject.toml"
        self.state_file = self.repo_root / ".branch_state.json"

    def _find_repo_root(self) -> Path:
        """Find the git repository root."""
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())

    def _run_git_command(self, *args) -> str:
        """Run a git command and return output."""
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def get_current_branch(self) -> str:
        """Get the current git branch name."""
        return self._run_git_command("rev-parse", "--abbrev-ref", "HEAD")

    def get_version_from_pyproject(self) -> str:
        """Extract version from pyproject.toml."""
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}")
        
        with open(self.pyproject_path, "r") as f:
            data = toml.load(f)
        
        version = data.get("project", {}).get("version")
        if not version:
            version = data.get("tool", {}).get("poetry", {}).get("version")
        
        if not version:
            raise ValueError("Version not found in pyproject.toml")
        
        return version

    def show_status(self):
        """Display current branch and version status."""
        current_branch = self.get_current_branch()
        current_version = self.get_version_from_pyproject()
        
        print(f"Current Branch: {current_branch}")
        print(f"Current Version: {current_version}")
        
        # Show git status
        try:
            status = self._run_git_command("status", "--short")
            if status:
                print("\nGit Status:")
                print(status)
            else:
                print("\nGit Status: Clean")
        except subprocess.CalledProcessError:
            print("Unable to get git status")

    def bump_version(self, new_version: str):
        """Update version in pyproject.toml."""
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}")
        
        with open(self.pyproject_path, "r") as f:
            data = toml.load(f)
        
        # Update version in project section
        if "project" in data:
            data["project"]["version"] = new_version
        
        # Update version in poetry section
        if "tool" in data and "poetry" in data["tool"]:
            data["tool"]["poetry"]["version"] = new_version
        
        with open(self.pyproject_path, "w") as f:
            toml.dump(data, f)
        
        print(f"Version bumped to {new_version}")

    def create_version_tag(self, version: str = None):
        """Create a git tag for the version."""
        if version is None:
            version = self.get_version_from_pyproject()
        
        tag_name = f"v{version}"
        
        try:
            self._run_git_command("tag", tag_name)
            print(f"Tag created: {tag_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create tag: {e}")
            raise

    def save_state(self):
        """Save current branch and version state to file."""
        state = {
            "branch": self.get_current_branch(),
            "version": self.get_version_from_pyproject(),
            "commit": self._run_git_command("rev-parse", "HEAD")
        }
        
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)
        
        print(f"State saved to {self.state_file}")