from __future__ import annotations

import json
import yaml
from pathlib import Path
from typing import Any, Dict, Union

# Assume ExtractionConfig is defined elsewhere in the same package.
# Import it here. If it's in the same module, adjust the import accordingly.
try:
    from .config import ExtractionConfig  # type: ignore
except Exception:
    # Fallback: try a direct import if the module name differs
    from extraction_config import ExtractionConfig  # type: ignore


def _load_yaml(data: str) -> Dict[str, Any]:
    """Parse YAML string into a dictionary."""
    return yaml.safe_load(data) or {}


def _load_json(data: str) -> Dict[str, Any]:
    """Parse JSON string into a dictionary."""
    return json.loads(data)


def _parse_config_file(file_path: Path) -> Dict[str, Any]:
    """Read and parse a configuration file based on its extension."""
    if not file_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    if file_path.suffix.lower() in {".yaml", ".yml"}:
        with file_path.open("r", encoding="utf-8") as f:
            return _load_yaml(f.read())
    elif file_path.suffix.lower() == ".json":
        with file_path.open("r", encoding="utf-8") as f:
            return _parse_config_file(f.read())
    else:
        # Try to guess format by content
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        try:
            return _load_yaml(content)
        except Exception:
            try:
                return _parse_config_file(content)
            except Exception as exc:
                raise ValueError(
                    f"Unsupported configuration format for file {file_path}"
                ) from exc


def load_config_from_path(config_path: Union[Path, str]) -> ExtractionConfig:
    """
    Load an ExtractionConfig instance from a file path.

    Parameters
    ----------
    config_path : Path | str
        Path to the configuration file. Supports YAML (.yaml, .yml) and JSON (.json) formats.

    Returns
    -------
    ExtractionConfig
        An instance of ExtractionConfig populated with the data from the file.

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist.
    ValueError
        If the file format is unsupported or the content cannot be parsed.
    """
    path = Path(config_path) if not isinstance(config_path, Path) else config_path

    # Load raw configuration dictionary
    raw_config = _parse_config_file(path)

    # Validate that the raw_config is a dictionary
    if not isinstance(raw_config, dict):
        raise ValueError(
            f"Configuration file {path} did not contain a mapping at the top level."
        )

    # Instantiate ExtractionConfig with the loaded data
    try:
        return ExtractionConfig(**raw_config)
    except TypeError as exc:
        raise ValueError(
            f"Failed to instantiate ExtractionConfig from {path}. "
            f"Check that the configuration keys match the expected fields."
        ) from exc