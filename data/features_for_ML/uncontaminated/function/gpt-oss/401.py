import datetime
from typing import Tuple

def _parse_time_part(part: str) -> datetime.time:
    """Parse a time string in HH:MM or HH:MM:SS format."""
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.datetime.strptime(part.strip(), fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Invalid time format: '{part}'")

def _split_range(range_str: str) -> Tuple[datetime.time, datetime.time]:
    """Split a range string into start and end times."""
    if "-" not in range_str:
        raise ValueError("Time range must contain a '-' separator")
    start_str, end_str = range_str.split("-", 1)
    start = _parse_time_part(start_str)
    end = _parse_time_part(end_str)
    return start, end

def is_current_time_within_range(time_range_str: str) -> bool:
    """
    Return True if the current local time falls within the specified time range.

    The time range string must be in the format "HH:MM-HH:MM" or
    "HH:MM:SS-HH:MM:SS".  Midnight wrap‑around is supported:
    e.g. "22:00-02:00" matches times from 22:00 to 23:59:59 and
    from 00:00 to 02:00.

    Raises ValueError for malformed input.
    """
    start, end = _split_range(time_range_str)

    now = datetime.datetime.now().time()

    if start <= end:
        return start <= now <= end
    # Wrap around midnight
    return now >= start or now <= end