import os
import re

def get_pattern_matches(folder, pattern):
    """Given all the files in the folder, find those that match the pattern.

    If there are groups defined, the groups are returned. Otherwise the path to the matches are returned.
    """
    matches = []
    compiled_pattern = re.compile(pattern)
    
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        match = compiled_pattern.search(filename)
        
        if match:
            if match.groups():
                matches.append(match.groups())
            else:
                matches.append(filepath)
    
    return matches