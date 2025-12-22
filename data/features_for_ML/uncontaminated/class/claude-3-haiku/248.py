import json
from pathlib import Path
from typing import Any, Dict, Optional

class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            self.config_dir = Path.home() / ".config"
        else:
            self.config_dir = config_dir
        self.last_used_file = self.config_dir / "last_used.json"

    def save(self, settings: "Settings") -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with self.last_used_file.open("w") as f:
            json.dump(settings.to_dict(), f)

    def load(self) -> Dict[str, Any]:
        if self.exists():
            with self.last_used_file.open("r") as f:
                return json.load(f)
        return {}

    def clear(self) -> None:
        if self.exists():
            self.last_used_file.unlink()

    def exists(self) -> bool:
        return self.last_used_file.exists()