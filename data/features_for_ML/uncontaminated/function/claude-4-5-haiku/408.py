def read_file_or_lookup_interface(root_path: Path, file_path: str) -> str:
    """Read the contents of a text file and return it as a string.

    If the file has more than {MAX_LINES} lines, return the module public interface
    lookup tool.
    """
    MAX_LINES = 100
    
    full_path = root_path / file_path
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) > MAX_LINES:
            return f"File {file_path} has {len(lines)} lines, which exceeds the maximum of {MAX_LINES} lines. Use the module public interface lookup tool to explore this file."
        
        return ''.join(lines)
    
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"