import json
from pathlib import Path
from typing import Any, Dict, Optional


class LastUsedParams:
    """Manages last used parameters persistence (moved from last_used.py)."""

    _FILENAME = "last_used.json"

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        """
        Initialize the LastUsedParams manager.

        Parameters
        ----------
        config_dir : Optional[Path]
            Directory where the last used parameters file will be stored.
            If None, defaults to a subdirectory named 'last_used_params'
            inside the current working directory.
        """
        if config_dir is None:
            config_dir = Path.cwd() / "last_used_params"
        self._config_dir = Path(config_dir).expanduser()
        self._file_path = self._config_dir / self._FILENAME

    def save(self, settings: "Settings") -> None:
        """
        Persist the given settings to the JSON file.

        Parameters
        ----------
        settings : Settings
            An object that can be converted to a dictionary via its
            ``__dict__`` attribute.  The method will store the dictionary
            representation of the settings.
        """
        try:
            self._config_dir.mkdir(parents=True, exist_ok=True)
            data = getattr(settings, "__dict__", {})
            with self._file_path.open("w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=2, sort_keys=True)
        except Exception:
            # Silently ignore any I/O errors; the caller can decide how to handle them.
            pass

    def load(self) -> Dict[str, Any]:
        """
        Load the last used parameters from the JSON file.

        Returns
        -------
        Dict[str, Any]
            The dictionary representation of the stored settings.  If the
            file does not exist or cannot be parsed, an empty dictionary
            is returned.
        """
        if not self._file_path.is_file():
            return {}
        try:
            with self._file_path.open("r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception:
            return {}

    def clear(self) -> None:
        """
        Remove the stored last used parameters file, if it exists.
        """
        try:
            if self._file_path.is_file():
                self._file_path.unlink()
        except Exception:
            pass

    def exists(self) -> bool:
        """
        Check whether the last used parameters file exists.

        Returns
        -------
        bool
            True if the file exists, False otherwise.
        """
        return self._file_path.is_file()