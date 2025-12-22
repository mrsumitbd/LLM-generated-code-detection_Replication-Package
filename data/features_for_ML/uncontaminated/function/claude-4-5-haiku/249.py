def format_local(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Format datetime in local timezone.

    Args:
        dt: Datetime to format
        format_str: Format string (default includes timezone)

    Returns:
        str: Formatted datetime string in local timezone
    """
    import pytz
    
    # If dt is naive, assume it's in UTC
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    
    # Convert to local timezone
    local_tz = pytz.timezone('UTC')
    try:
        import time
        if time.daylight:
            local_tz = pytz.timezone('UTC')
        local_dt = dt.astimezone()
    except:
        local_dt = dt.astimezone()
    
    return local_dt.strftime(format_str)