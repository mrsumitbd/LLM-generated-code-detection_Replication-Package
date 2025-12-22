import os
import json
import pathlib
from datetime import datetime

try:
    import toml
except ImportError:
    import tomllib as toml  # Python 3.11+

class ConfigManager:
    """Handles loading, accessing, and updating the Pylings configuration from `pylings.toml`."""

    DEFAULT_CONFIG = {
        "lasttime_exercise": None,
        "solutions": {},
        "hints": {},
        "solution_dir": "solutions",
    }

    def __init__(self):
        self.config_path = pathlib.Path("pylings.toml")
        self._first_time = not self.config_path.exists()
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self):
        """Load configuration from the TOML file, creating defaults if necessary."""
        if self.config_path.exists():
            try:
                with self.config_path.open("rb") as f:
                    self.config = toml.load(f)
            except Exception:
                # Corrupted file – reset to defaults
                self.config = self.DEFAULT_CONFIG.copy()
                self._write_config()
        else:
            self.config = self.DEFAULT_CONFIG.copy()
            self._write_config()

    def _write_config(self):
        """Write the current configuration to disk."""
        with self.config_path.open("w", encoding="utf-8") as f:
            toml.dump(self.config, f)

    def check_first_time(self):
        """Return True if this is the first time the config file was created."""
        return self._first_time

    def get_lasttime_exercise(self):
        """Return the last exercise that was run, or None."""
        return self.config.get("lasttime_exercise")

    def set_lasttime_exercise(self, current_exercise):
        """Record the current exercise as the last one run."""
        self.config["lasttime_exercise"] = current_exercise
        self._write_config()

    def get_local_solution_path(self, solution_path):
        """
        Resolve a solution path relative to the configured solution directory.
        If the path is already absolute, it is returned unchanged.
        """
        base_dir = pathlib.Path(self.config.get("solution_dir", "solutions"))
        path = pathlib.Path(solution_path)
        if not path.is_absolute():
            path = base_dir / path
        return path.resolve()

    def get_hint(self, current_exercise):
        """Return the hint string for the given exercise, or None if not defined."""
        return self.config.get("hints", {}).get(current_exercise)