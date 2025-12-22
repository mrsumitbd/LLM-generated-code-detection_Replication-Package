from pathlib import Path

MAX_LINES = 100

def read_file_or_lookup_interface(root_path: Path, file_path: str) -> str:
    file_path = root_path / file_path
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) > MAX_LINES:
                return "module public interface lookup tool"
            else:
                return ''.join(lines)
    except FileNotFoundError:
        return "module public interface lookup tool"