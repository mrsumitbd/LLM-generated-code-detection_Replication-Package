from datetime import datetime

def format_local(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    """
    Format datetime in local timezone.

    Args:
        dt: Datetime to format
        format_str: Format string (default includes timezone)

    Returns:
        str: Formatted datetime string in local timezone
    """
    # If dt is naive, attach the local timezone
    if dt.tzinfo is None:
        local_tz = datetime.now().astimezone().tzinfo
        dt = dt.replace(tzinfo=local_tz)
    else:
        # Convert to local timezone
        dt = dt.astimezone()
    return dt.strftime(format_str)