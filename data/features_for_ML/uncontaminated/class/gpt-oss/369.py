import subprocess
import pathlib
import re
import sys
from typing import Optional

class BranchManager:
    """Manages versions across main and mcp-remote branches safely."""

    def __init__(self, repo_path: Optional[pathlib.Path] = None):
        self.repo_path = pathlib.Path(repo_path or pathlib.Path.cwd()).resolve()
        if not (self.repo_path / ".git").exists():
            raise RuntimeError(f"No .git directory found in {self.repo_path}")

    def _run(self, args, capture_output=True, check=True):
        result = subprocess.run(
            args,
            cwd=self.repo_path,
            text=True,
            capture_output=capture_output,
            check=check,
        )
        return result.stdout.strip() if capture_output else None

    def get_current_branch(self) -> str:
        """Return the name of the current git branch."""
        return self._run(["git", "rev-parse", "--abbrev-ref", "HEAD"])

    def get_version_from_pyproject(self) -> str:
        """Read the version from pyproject.toml."""
        pyproject = self.repo_path / "pyproject.toml"
        if not pyproject.exists():
            raise FileNotFoundError(f"{pyproject} does not exist")
        content = pyproject.read_text(encoding="utf-8")
        # Try Poetry style
        m = re.search(r'\[tool\.poetry\]\s*version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if m:
            return m.group(1)
        # Try PEP 621 style
        m = re.search(r'\[project\]\s*version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if m:
            return m.group(1)
        raise ValueError("Could not find version in pyproject.toml")

    def show_status(self):
        """Print current branch, version, and git status."""
        branch = self.get_current_branch()
        try:
            version = self.get_version_from_pyproject()
        except Exception:
            version = "<unknown>"
        status = self._run(["git", "status", "--short"])
        print(f"Branch: {branch}")
        print(f"Version: {version}")
        print("Git status:")
        print(status or "(clean)")

    def bump_version(self, new_version: str):
        """Update the version in pyproject.toml to new_version."""
        pyproject = self.repo_path / "pyproject.toml"
        if not pyproject.exists():
            raise FileNotFoundError(f"{pyproject} does not exist")
        content = pyproject.read_text(encoding="utf-8")

        def replace_version(match):
            return f'{match.group(1)}"{new_version}"'

        # Poetry
        content, count = re.subn(
            r'(version\s*=\s*")([^"]+)(")', replace_version, content
        )
        # PEP 621
        if count == 0:
            content, count = re.subn(
                r'(version\s*=\s*")([^"]+)(")', replace_version, content
            )
        if count == 0:
            raise ValueError("Could not find a version entry to replace")

        pyproject.write_text(content, encoding="utf-8")
        # Commit the change
        self._run(["git", "add", "pyproject.toml"])
        self._run(
            ["git", "commit", "-m", f"Bump version to {new_version}"], check=False
        )
        print(f"Bumped version to {new_version} and committed.")

    def create_version_tag(self, version: Optional[str] = None):
        """Create an annotated git tag for the given version."""
        if version is None:
            version = self.get_version_from_pyproject()
        tag_name = f"v{version}"
        # Check if tag already exists
        existing = self._run(["git", "tag"], capture_output=True, check=False)
        if tag_name in existing.splitlines():
            print(f"Tag {tag_name} already exists.")
            return
        self._run(
            ["git", "tag", "-a", tag_name, "-m", f"Release {tag_name}"],
            check=True,
        )
        self._run(["git", "push", "origin", tag_name], check=True)
        print(f"Created and pushed tag {tag_name}.")

    def save_state(self):
        """Ensure all changes are committed and pushed."""
        # Stage all changes
        self._run(["git", "add", "."], check=False)
        # Commit if there are changes
        diff = self._run(["git", "diff", "--cached", "--quiet"], check=False)
        if diff is None:
            # No changes staged
            print("No changes to commit.")
        else:
            self._run(
                ["git", "commit", "-m", "Auto-save state"], check=False
            )
            print("Committed staged changes.")
        # Push current branch
        branch = self.get_current_branch()
        self._run(["git", "push", "origin", branch], check=True)
        print(f"Pushed branch {branch} to origin.")