import json
from pathlib import Path
from typing import TypedDict

class ConfigDict(TypedDict):
    name: str
    age: int
    species: str
    color: str

def load_config(configs_dir: Path, pet_name: str) -> ConfigDict:
    config_file = configs_dir / f"{pet_name}.json"
    
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    return ConfigDict(
        name=config_data['name'],
        age=config_data['age'],
        species=config_data['species'],
        color=config_data['color']
    )