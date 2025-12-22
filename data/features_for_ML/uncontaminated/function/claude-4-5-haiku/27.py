def parse_key_value_format(text):
    """
    Parse the Key|Value format from the submission body.
    This handles both the expected format from label.txt and the submission format.
    """
    result = {}
    if not text:
        return result
    
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or '|' not in line:
            continue
        
        parts = line.split('|', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            result[key] = value
    
    return result