class BranchManager:
    """Manages versions across main and mcp-remote branches safely."""

    def __init__(self):
        self.current_branch = "main"
        self.version = ""

    def get_current_branch(self) -> str:
        return self.current_branch

    def get_version_from_pyproject(self) -> str:
        # Assume this method reads the version from a pyproject file
        # For demonstration purposes, we will return a hardcoded version
        return "1.0.0"

    def show_status(self):
        print(f"Current branch: {self.current_branch}")
        print(f"Current version: {self.version}")

    def bump_version(self, new_version: str):
        self.version = new_version

    def create_version_tag(self, version: str = None):
        if version is None:
            version = self.version
        print(f"Creating tag for version {version}")

    def save_state(self):
        # Assume this method saves the current state of the BranchManager
        print("Saving state...")