from pathlib import Path
from typing import Dict

def load_config(configs_dir: Path, pet_name: str) -> Dict:
    config_file = configs_dir / f"{pet_name}.json"
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    return config_data