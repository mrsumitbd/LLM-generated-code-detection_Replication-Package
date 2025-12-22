from typing import Dict
from pathlib import Path

def get_file_content(filepath: Path) -> Dict[str, str]:
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return {'content': content}
    except IOError as e:
        raise IOError(f"Failed to read content of {filepath}") from e