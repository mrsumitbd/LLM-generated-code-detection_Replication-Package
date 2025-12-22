import os
import re

def get_pattern_matches(folder, pattern):
    """Given all the files in the folder, find those that match the pattern.

    If there are groups defined, the groups are returned. Otherwise the path to the matches are returned.
    """
    if not isinstance(folder, str):
        raise TypeError("folder must be a string path")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")

    # Compile the pattern as a regular expression
    regex = re.compile(pattern)

    # Determine if the pattern contains capturing groups
    has_groups = regex.groups > 0

    matches = []

    try:
        entries = os.listdir(folder)
    except OSError as e:
        raise FileNotFoundError(f"Cannot list directory '{folder}': {e}") from e

    for entry in entries:
        full_path = os.path.join(folder, entry)
        if not os.path.isfile(full_path):
            continue

        m = regex.search(entry)
        if m:
            if has_groups:
                matches.append(m.groups())
            else:
                matches.append(full_path)

    return matches