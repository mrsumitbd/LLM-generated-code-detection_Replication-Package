def parse_key_value_format(text):
    """
    Parse the Key|Value format from the submission body.
    This handles both the expected format from label.txt and the submission format.
    """
    key_value_pairs = {}
    for line in text.splitlines():
        if '|' in line:
            key, value = line.split('|', 1)
            key_value_pairs[key.strip()] = value.strip()
    return key_value_pairs