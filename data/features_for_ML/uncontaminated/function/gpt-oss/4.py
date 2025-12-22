import re

def fix_fracs(string):
    """
    Remove any whitespace surrounding a slash in the input string.
    This standardises fractions such as "1 / 2", "1/ 2", or "1 /2" to "1/2".
    """
    return re.sub(r'\s*/\s*', '/', string)