import os
import tomllib
from pathlib import Path


class ConfigManager:
    """Handles loading, accessing, and updating the Pylings configuration from `pylings.toml`."""

    def __init__(self):
        self.config_path = Path.home() / ".pylings" / "pylings.toml"
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from pylings.toml file."""
        if self.config_path.exists():
            with open(self.config_path, "rb") as f:
                self.config = tomllib.load(f)
        else:
            self.config = {
                "progress": {},
                "last_exercise": None,
                "first_time": True
            }
            self._save_config()

    def _save_config(self):
        """Save configuration to pylings.toml file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        import toml
        with open(self.config_path, "w") as f:
            toml.dump(self.config, f)

    def check_first_time(self):
        """Check if this is the first time running Pylings."""
        is_first_time = self.config.get("first_time", True)
        if is_first_time:
            self.config["first_time"] = False
            self._save_config()
        return is_first_time

    def get_lasttime_exercise(self):
        """Get the last exercise that was being worked on."""
        return self.config.get("last_exercise", None)

    def set_lasttime_exercise(self, current_exercise):
        """Set the last exercise being worked on."""
        self.config["last_exercise"] = current_exercise
        self._save_config()

    def get_local_solution_path(self, solution_path):
        """Get the local path for a solution file."""
        pylings_dir = Path.home() / ".pylings"
        pylings_dir.mkdir(parents=True, exist_ok=True)
        
        solution_name = Path(solution_path).name
        local_path = pylings_dir / "solutions" / solution_name
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        return str(local_path)

    def get_hint(self, current_exercise):
        """Get the hint for a specific exercise."""
        if "exercises" in self.config and current_exercise in self.config["exercises"]:
            return self.config["exercises"][current_exercise].get("hint", "No hint available")
        return "No hint available"