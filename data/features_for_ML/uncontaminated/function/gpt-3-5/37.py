from pathlib import Path

def load_config_from_path(config_path: Path | str) -> ExtractionConfig:
    if isinstance(config_path, str):
        config_path = Path(config_path)
    
    with open(config_path, 'r') as file:
        config_data = json.load(file)
    
    extraction_config = ExtractionConfig(**config_data)
    
    return extraction_config