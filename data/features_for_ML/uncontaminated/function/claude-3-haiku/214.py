from pathlib import Path
from typing import Dict

ConfigDict = Dict[str, any]

def load_config(configs_dir: Path, pet_name: str) -> ConfigDict:
    config_file = configs_dir / f"{pet_name}.json"
    with config_file.open("r") as f:
        config = json.load(f)
    return config