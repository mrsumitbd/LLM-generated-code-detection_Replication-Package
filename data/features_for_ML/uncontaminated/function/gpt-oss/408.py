from pathlib import Path

# Default maximum number of lines before falling back to the lookup tool.
# If a project defines its own MAX_LINES, it can override this value.
MAX_LINES = 1000

def read_file_or_lookup_interface(root_path: Path, file_path: str) -> str:
    """
    Read the contents of a text file and return it as a string.

    If the file has more than {MAX_LINES} lines, return the module public
    interface lookup tool.
    """
    # Resolve the full path to the file
    full_path = root_path / file_path

    # Ensure the file exists and is a file
    if not full_path.is_file():
        raise FileNotFoundError(f"File not found: {full_path}")

    # Read the file line by line to avoid loading huge files entirely into memory
    line_count = 0
    content_lines = []

    with full_path.open(encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if line_count > MAX_LINES:
                # Too many lines – return the lookup tool placeholder
                return "module public interface lookup tool"
            content_lines.append(line)

    # Join the lines back into a single string
    return "".join(content_lines)