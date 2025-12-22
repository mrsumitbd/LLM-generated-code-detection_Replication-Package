import os
from pathlib import Path

def is_valid_db(dir_in: Path) -> bool:
    """
    Checks if the input directory is a valid typing database.
    :param dir_in: Input directory
    :return: True if valid
    """
    if not dir_in.is_dir():
        return False

    required_files = ['words.txt', 'metadata.json']
    for file in required_files:
        if not (dir_in / file).is_file():
            return False

    try:
        with open(dir_in / 'words.txt', 'r') as f:
            word_count = len(f.readlines())
        if word_count < 1000:
            return False
    except (OSError, IOError):
        return False

    return True