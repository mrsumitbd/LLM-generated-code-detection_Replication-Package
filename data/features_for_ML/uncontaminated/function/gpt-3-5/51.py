def utc_timestamp(
    precise: bool = False,
    env_var: str = "BUILD_TIMESTAMP",
    fallback: str = "2024-01-01T00:00:00Z",
) -> str:
    import os
    from datetime import datetime

    timestamp = os.getenv(env_var, fallback)

    if 'Z' not in timestamp:
        timestamp += 'Z'

    try:
        dt = datetime.fromisoformat(timestamp)
        if not precise:
            dt = dt.replace(microsecond=0)
        return dt.isoformat(timespec='microseconds') if precise else dt.isoformat()
    except ValueError:
        return fallback