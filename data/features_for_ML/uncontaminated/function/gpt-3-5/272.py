def parse_directory_structure(data: str) -> dict:
    lines = data.split('\n')
    result = {}
    for line in lines:
        directories = line.split('/')
        current_dir = result
        for directory in directories:
            if directory not in current_dir:
                current_dir[directory] = 0
            current_dir[directory] += 1
            current_dir = current_dir[directory]
    return result