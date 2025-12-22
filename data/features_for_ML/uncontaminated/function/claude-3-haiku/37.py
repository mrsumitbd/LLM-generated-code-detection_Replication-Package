from pathlib import Path
from typing import Union
from pydantic import BaseModel

class ExtractionConfig(BaseModel):
    """
    Pydantic model for the extraction configuration.
    """
    input_directory: Path
    output_directory: Path
    file_extensions: list[str]
    max_file_size: int

def load_config_from_path(config_path: Union[Path, str]) -> ExtractionConfig:
    """
    Load the extraction configuration from the specified file path.

    Args:
        config_path (Union[Path, str]): The path to the configuration file.

    Returns:
        ExtractionConfig: The loaded extraction configuration.
    """
    if isinstance(config_path, str):
        config_path = Path(config_path)

    with config_path.open("r") as config_file:
        config_data = config_file.read()

    return ExtractionConfig.parse_raw(config_data)