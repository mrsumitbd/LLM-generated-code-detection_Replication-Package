import datetime

def is_current_time_within_range(time_range_str: str) -> bool:
    """
    Checks if the current time is within the specified time range.

    Args:
        time_range_str (str): A string representing the time range in the format "HH:MM-HH:MM".

    Returns:
        bool: True if the current time is within the specified time range, False otherwise.
    """
    try:
        start_time, end_time = time_range_str.split('-')
        start_hour, start_minute = map(int, start_time.split(':'))
        end_hour, end_minute = map(int, end_time.split(':'))

        current_time = datetime.datetime.now().time()
        start_time = datetime.time(start_hour, start_minute)
        end_time = datetime.time(end_hour, end_minute)

        if end_time < start_time:
            return current_time >= start_time or current_time < end_time
        else:
            return start_time <= current_time < end_time
    except (ValueError, IndexError):
        return False