def parse_directory_structure(data: str) -> dict:
    """
    Parses the directory structure string and returns a dictionary where:
      - Keys: directory names
      - Values: count of files in that directory.
    """
    directory_counts = {}
    for line in data.splitlines():
        if line.startswith(' '):
            continue
        directory = line.split('/')[0]
        if directory in directory_counts:
            directory_counts[directory] += 1
        else:
            directory_counts[directory] = 1
    return directory_counts