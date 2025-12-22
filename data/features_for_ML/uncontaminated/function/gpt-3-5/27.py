def parse_key_value_format(text):
    key_value_pairs = {}
    lines = text.split('\n')
    for line in lines:
        if '|' in line:
            key, value = line.split('|', 1)
            key = key.strip()
            value = value.strip()
            key_value_pairs[key] = value
    return key_value_pairs