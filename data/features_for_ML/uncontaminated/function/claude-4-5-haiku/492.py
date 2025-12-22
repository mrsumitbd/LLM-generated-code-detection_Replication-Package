def is_valid_db(dir_in: Path) -> bool:
    """
    Checks if the input directory is a valid typing database.
    :param dir_in: Input directory
    :return: True if valid
    """
    if not dir_in.is_dir():
        return False
    
    required_files = ['metadata.json', 'data.json']
    for file in required_files:
        if not (dir_in / file).is_file():
            return False
    
    return True