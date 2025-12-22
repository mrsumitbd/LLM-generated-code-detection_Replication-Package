import re
from typing import Dict

def parse_directory_structure(data: str) -> Dict[str, int]:
    """
    Parses the directory structure string and returns a dictionary where:
      - Keys: directory names
      - Values: count of files in that directory.
    """
    result: Dict[str, int] = {}
    stack: list[tuple[str, int]] = []  # (dir_name, indent_level)

    for raw_line in data.splitlines():
        line = raw_line.rstrip('\n')
        if not line.strip():
            continue  # skip empty lines

        # Determine indentation level (number of leading spaces or tabs)
        m = re.match(r'^([ \t]*)', line)
        indent = len(m.group(1)) if m else 0
        name = line.lstrip()

        # Pop stack until we find the parent level
        while stack and stack[-1][1] >= indent:
            stack.pop()

        if name.endswith('/'):  # directory
            dir_name = name.rstrip('/')
            result[dir_name] = 0
            stack.append((dir_name, indent))
        else:  # file
            if stack:
                parent_dir = stack[-1][0]
                result[parent_dir] = result.get(parent_dir, 0) + 1
            else:
                # File at the root level without an explicit root directory
                # Use a special key for root if desired; here we skip it
                pass

    return result