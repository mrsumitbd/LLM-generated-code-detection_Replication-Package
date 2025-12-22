def get_pattern_matches(folder, pattern):
    import os
    import re

    matches = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if re.match(pattern, file):
                matches.append(os.path.join(root, file))

    return matches