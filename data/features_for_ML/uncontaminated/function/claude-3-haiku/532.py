import os
import re

def get_pattern_matches(folder, pattern):
    """Given all the files in the folder, find those that match the pattern.

    If there are groups defined, the groups are returned. Otherwise the path to the matches are returned.
    """
    matches = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            match = re.search(pattern, filename)
            if match:
                if match.groups():
                    matches.append(match.groups())
                else:
                    matches.append(file_path)
    return matches