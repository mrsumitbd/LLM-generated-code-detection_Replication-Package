def timestamp_to_seconds(timestamp):
    """
    Convert a timestamp string into the total number of seconds.

    The function accepts timestamps in the following formats:
        - "SS"
        - "MM:SS"
        - "HH:MM:SS"
        - "DD:HH:MM:SS"
    Any leading zeros are allowed. The function returns an integer number of seconds.

    Parameters
    ----------
    timestamp : str
        The timestamp string to convert.

    Returns
    -------
    int
        The total number of seconds represented by the timestamp.

    Raises
    ------
    ValueError
        If the timestamp format is invalid or contains non‑numeric components.
    """
    if not isinstance(timestamp, str):
        raise ValueError("timestamp must be a string")

    parts = timestamp.split(":")
    if not parts:
        raise ValueError("empty timestamp")

    # Convert each part to an integer, ensuring they are numeric
    try:
        nums = [int(part) for part in parts]
    except ValueError:
        raise ValueError("timestamp contains non-numeric parts")

    # Validate that each part is non-negative
    if any(n < 0 for n in nums):
        raise ValueError("timestamp contains negative values")

    # Compute seconds based on the number of parts
    # The rightmost part is seconds, then minutes, hours, days, etc.
    total_seconds = 0
    multiplier = 1  # seconds
    for n in reversed(nums):
        total_seconds += n * multiplier
        multiplier *= 60

    return total_seconds