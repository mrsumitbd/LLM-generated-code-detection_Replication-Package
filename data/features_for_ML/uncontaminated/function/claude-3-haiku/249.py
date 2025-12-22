import pytz
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
    local_tz = pytz.timezone('UTC').localize(dt).astimezone(pytz.local_timezone())
    return local_tz.strftime(format_str)