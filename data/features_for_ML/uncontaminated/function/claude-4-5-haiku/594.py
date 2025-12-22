def timestamp_to_seconds(timestamp):
    """Convert a timestamp string to seconds.
    
    Supports formats like:
    - "1h 30m 45s" -> 5445 seconds
    - "2:30:45" -> 9045 seconds
    - "45s" -> 45 seconds
    - "30m" -> 1800 seconds
    - "1h" -> 3600 seconds
    """
    if not timestamp or not isinstance(timestamp, str):
        return 0
    
    timestamp = timestamp.strip()
    total_seconds = 0
    
    # Handle HH:MM:SS format
    if ':' in timestamp and not any(c in timestamp for c in ['h', 'm', 's']):
        parts = timestamp.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = parts
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        elif len(parts) == 2:
            minutes, seconds = parts
            total_seconds = int(minutes) * 60 + int(seconds)
        return total_seconds
    
    # Handle format like "1h 30m 45s"
    import re
    
    # Find all number-unit pairs
    pattern = r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)'
    matches = re.findall(pattern, timestamp)
    
    for value, unit in matches:
        value = float(value)
        unit = unit.lower().strip()
        
        if unit.startswith('h'):
            total_seconds += value * 3600
        elif unit.startswith('m'):
            total_seconds += value * 60
        elif unit.startswith('s'):
            total_seconds += value
    
    return int(total_seconds)