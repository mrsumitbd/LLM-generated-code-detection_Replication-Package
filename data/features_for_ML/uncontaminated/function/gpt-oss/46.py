import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

# Global configuration dictionary that will be updated by this function.
CONFIG: Dict[str, Any] = {}


def _load_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load a JSON configuration file and return its contents as a dict."""
    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def apply_config_file(
    config_path: str | None = None,
    search_paths: list[str] | None = None,
    file_names: list[str] | None = None,
) -> bool:
    """
    Find and apply configuration from a file.

    Args:
        config_path: Explicit path to config file, takes precedence if provided
        search_paths: List of directories to search for config files
        file_names: List of file names to search for

    Returns:
        True if configuration was loaded and applied, False otherwise
    """
    # Helper to attempt loading a file and applying it
    def _try_load_and_apply(path: Path) -> bool:
        data = _load_json(path)
        if data is None:
            return False
        # Merge the loaded data into the global CONFIG
        CONFIG.update(data)
        return True

    # 1. If an explicit config path is given, try it first
    if config_path:
        explicit_path = Path(config_path).expanduser().resolve()
        if explicit_path.is_file():
            return _try_load_and_apply(explicit_path)

    # 2. If no explicit path or it failed, search in provided directories
    if search_paths and file_names:
        for dir_path in search_paths:
            base_dir = Path(dir_path).expanduser().resolve()
            if not base_dir.is_dir():
                continue
            for name in file_names:
                candidate = base_dir / name
                if candidate.is_file():
                    if _try_load_and_apply(candidate):
                        return True

    # 3. No configuration found
    return False