from typing import Literal, Optional, TypedDict, Dict, Any, List, Tuple, Union
from pathlib import Path

def get_file_content(
    filepath: Path
) -> Dict[str, str]:
    """
    Get content of a file.
    Args:
        filepath: Path to a file
    Returns:
        A string containing file content
    Raises:
        IOError: if read content of `filepath` failed
    """
    filepath = Path(filepath)
    file_content = ''
    try:
        with open(filepath) as fin:
            for lines in fin:
                file_content += lines
    except:
        raise IOError(f"Read content of {filepath} failed")
    
    max_length = 2000
    if len(file_content) > max_length:
        file_content = file_content[:max_length]
    return {'file_content': file_content}