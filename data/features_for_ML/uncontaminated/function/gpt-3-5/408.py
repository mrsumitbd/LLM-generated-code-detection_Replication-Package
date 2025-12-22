def read_file_or_lookup_interface(root_path: Path, file_path: str) -> str:
    MAX_LINES = 1000
    file_full_path = root_path / file_path
    with open(file_full_path, 'r') as file:
        lines = file.readlines()
        if len(lines) > MAX_LINES:
            return "Module public interface lookup tool"
        else:
            return ''.join(lines)