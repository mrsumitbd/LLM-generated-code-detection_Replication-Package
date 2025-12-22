from datetime import datetime

def format_local(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
    return dt.strftime(format_str)