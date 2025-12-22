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
    local_dt = to_local(dt)
    return local_dt.strftime(format_str)