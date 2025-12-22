def timestamp_to_seconds(timestamp):
    """
    Converts a timestamp string in the format 'YYYY-MM-DD HH:MM:SS' to the number of seconds since the Unix epoch.
    
    Args:
        timestamp (str): A timestamp string in the format 'YYYY-MM-DD HH:MM:SS'.
    
    Returns:
        int: The number of seconds since the Unix epoch.
    """
    from datetime import datetime
    
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return int(dt.timestamp())