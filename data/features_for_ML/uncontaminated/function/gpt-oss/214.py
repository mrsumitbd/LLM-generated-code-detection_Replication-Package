import json
from pathlib import Path
from typing import Any, Dict

# Assuming ConfigDict is a type alias for a dictionary with string keys
# and arbitrary values. If a different definition exists elsewhere,
# this alias can be overridden by importing that definition.
ConfigDict = Dict[str, Any]


def load_config(configs_dir: Path, pet_name: str) -> ConfigDict:
    """
    Load a configuration dictionary for the given pet name from the specified
    configuration directory.

    The function looks for configuration files in the following order:
    1. configs_dir / pet_name / "config.json"
    2. configs_dir / pet_name / "config.yaml" (if PyYAML is available)
    3. configs_dir / f"{pet_name}.json"
    4. configs_dir / f"{pet_name}.yaml" (if PyYAML is available)

    Raises:
        FileNotFoundError: If no configuration file is found.
        ValueError: If the configuration file cannot be parsed.
    """
    # Helper to load JSON
    def _load_json(path: Path) -> ConfigDict:
        try:
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in configuration file {path}") from exc

    # Helper to load YAML if available
    def _load_yaml(path: Path) -> ConfigDict:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("PyYAML is required to load YAML configuration files") from exc

        try:
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid YAML in configuration file {path}") from exc

    # Candidate paths
    candidates = [
        configs_dir / pet_name / "config.json",
        configs_dir / pet_name / "config.yaml",
        configs_dir / f"{pet_name}.json",
        configs_dir / f"{pet_name}.yaml",
    ]

    for path in candidates:
        if not path.is_file():
            continue

        if path.suffix.lower() in {".json"}:
            return _load_json(path)
        if path.suffix.lower() in {".yaml", ".yml"}:
            return _load_yaml(path)

    # If we reach here, no config file was found
    raise FileNotFoundError(
        f"No configuration file found for pet '{pet_name}' in directory '{configs_dir}'. "
        f"Tried paths: {', '.join(str(p) for p in candidates)}"
    )