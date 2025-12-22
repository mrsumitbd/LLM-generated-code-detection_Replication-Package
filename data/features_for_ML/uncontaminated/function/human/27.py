def parse_key_value_format(text):
    """
    Parse the Key|Value format from the submission body.
    This handles both the expected format from label.txt and the submission format.
    """
    data = {}
    
    # Split by lines and parse each line
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Remove bullet point if present
        if line.startswith('- '):
            line = line[2:]
        elif line.startswith('• '):
            line = line[2:]
            
        # Parse pipe-separated format
        if '|' in line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                if value and value != 'FILL_VALUE':
                    data[key] = value
    
    return data