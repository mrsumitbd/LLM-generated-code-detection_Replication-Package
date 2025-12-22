import json
from pathlib import Path

def load_config(configs_dir: Path, pet_name: str) -> ConfigDict:
    path = configs_dir / f"{pet_name}.json"
    if path.is_file():
        with open(path, "r") as f:
            try:
                return (
                    ConfigDict()
                    .nested_update(ConfigDict.DEFAULTS, touch=True)
                    .nested_update(json.load(f), touch=False)
                )
            except Exception as e:
                logger.exception(f"Error loading config from {path}: {e}")

    return ConfigDict().nested_update(ConfigDict.DEFAULTS, touch=True)