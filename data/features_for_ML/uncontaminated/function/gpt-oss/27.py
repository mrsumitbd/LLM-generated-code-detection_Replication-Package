import re
from typing import Dict

def parse_key_value_format(text: str) -> Dict[str, str]:
    """
    Parse the Key|Value format from the submission body.
    This handles both the expected format from label.txt and the submission format.
    """
    result: Dict[str, str] = {}
    # Regular expression to split on the first occurrence of | or :
    # It also allows optional whitespace around the separator.
    pattern = re.compile(r'^(?P<key>[^|:]+?)\s*(?P<sep>[|:])\s*(?P<value>.*)$')

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Skip comment lines
        if line.startswith('#'):
            continue

        match = pattern.match(line)
        if not match:
            continue

        key = match.group('key').strip()
        value = match.group('value').strip()
        if key:
            result[key] = value

    return result