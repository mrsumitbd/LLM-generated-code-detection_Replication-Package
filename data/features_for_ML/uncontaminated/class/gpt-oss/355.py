import os
import sys
import json
import secrets
import tempfile
import glob
from pathlib import Path
from typing import Optional, Dict, List

class StorageManager:
    def __init__(self):
        self._temp_dir = Path(tempfile.gettempdir()) / "storage_manager_temp"
        self._temp_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Path helpers
    # ------------------------------------------------------------------
    def get_executable_path(self) -> str:
        """Return the path to the running executable or script."""
        return sys.executable if self.is_frozen() else os.path.abspath(__file__)

    def get_base_path(self) -> str:
        """Return the base directory of the application."""
        if self.is_frozen():
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def is_frozen(self) -> bool:
        """Return True if the application is frozen (e.g., PyInstaller)."""
        return getattr(sys, "frozen", False)

    def is_running_from_source(self) -> bool:
        """Return True if the application is running from source."""
        return not self.is_frozen()

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------
    def _verify_and_merge_config(
        self, original: Optional[Dict], new_data: Optional[Dict]
    ) -> Dict:
        """Merge two dictionaries, giving precedence to new_data."""
        base = original.copy() if original else {}
        if new_data:
            base.update(new_data)
        return base

    def _generate_key(self, path_root: str = "base", sub_path: str = "save") -> None:
        """Generate a random 32‑byte key and store it in a file."""
        key = secrets.token_bytes(32)
        key_path = self.get_path(path_root, sub_path) / "key.bin"
        key_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.write_bytes(key)

    def _load_key(self, path_root: str = "base", sub_path: str = "save") -> Optional[bytes]:
        """Load the key from the key file if it exists."""
        key_path = self.get_path(path_root, sub_path) / "key.bin"
        if key_path.is_file():
            return key_path.read_bytes()
        return None

    def get_path(
        self, path_root: str = "base", relative_path: Optional[str] = None
    ) -> Optional[str]:
        """Return an absolute path for a given root and relative path."""
        base = Path(self.get_base_path())
        root = base / path_root
        if relative_path:
            return str(root / relative_path)
        return str(root)

    def get_existing_path(
        self, path_root: str = "base", relative_path: Optional[str] = None
    ) -> Optional[str]:
        """Return the path only if it exists."""
        path = self.get_path(path_root, relative_path)
        if path and Path(path).exists():
            return path
        return None

    def save_config(
        self,
        path_root: str = "base",
        sub_path: str = "save",
        new: Optional[Dict] = None,
        original: Optional[Dict] = None,
    ) -> None:
        """Merge and save configuration to a JSON file."""
        config = self._verify_and_merge_config(original, new)
        config_path = Path(self.get_path(path_root, sub_path))
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, sort_keys=True)

    def load_config(
        self,
        path_root: str = "base",
        sub_path: str = "save",
        original: Optional[Dict] = None,
    ) -> Dict:
        """Load configuration from a JSON file and merge with original."""
        config_path = Path(self.get_path(path_root, sub_path))
        if config_path.is_file():
            with config_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
        else:
            loaded = {}
        return self._verify_and_merge_config(original, loaded)

    # ------------------------------------------------------------------
    # File helpers
    # ------------------------------------------------------------------
    def delete_file(
        self, path_root: str = "base", relative_path: Optional[str] = None
    ) -> bool:
        """Delete a file if it exists."""
        path = self.get_path(path_root, relative_path)
        if path and Path(path).is_file():
            Path(path).unlink()
            return True
        return False

    # ------------------------------------------------------------------
    # Temporary file helpers
    # ------------------------------------------------------------------
    def create_temp_txt(self, content: str = "") -> str:
        """Create a temporary text file with the given content."""
        tmp_file = self._temp_dir / f"temp_{secrets.token_hex(8)}.txt"
        tmp_file.write_text(content, encoding="utf-8")
        return str(tmp_file)

    def get_temp_files(self) -> List[str]:
        """Return a list of all temporary files."""
        return [str(p) for p in self._temp_dir.glob("*.txt")]

    def get_last_temp_file(self) -> Optional[str]:
        """Return the most recently created temporary file."""
        files = self.get_temp_files()
        if not files:
            return None
        return max(files, key=os.path.getctime)

    # ------------------------------------------------------------------
    # Misc helpers
    # ------------------------------------------------------------------
    def get_latest_version(self) -> Optional[str]:
        """Return the content of a 'version.txt' file in the base directory."""
        version_file = Path(self.get_path("base", "version.txt"))
        if version_file.is_file():
            return version_file.read_text(encoding="utf-8").strip()
        return None