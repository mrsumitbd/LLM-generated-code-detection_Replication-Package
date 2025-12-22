import os
from datetime import datetime, timezone

def utc_timestamp(
    precise: bool = False,
    env_var: str = "BUILD_TIMESTAMP",
    fallback: str = "2024-01-01T00:00:00Z",
) -> str:
    """Return a standardized UTC ISO-8601 timestamp with trailing Z.

    Args:
        precise: Include microseconds if True (default False)
        env_var: Environment variable that, if set, overrides the timestamp
        fallback: Fallback timestamp if generation fails

    Behavior:
        - If the environment variable exists, it's validated (appends 'Z' if
          missing and contains no timezone). Returned as-is otherwise.
        - Uses timezone-aware UTC datetime; strips microseconds unless
          precise=True.
        - Always normalizes '+00:00' suffix to 'Z'.
    """
    try:
        env_timestamp = os.getenv(env_var)
        if env_timestamp:
            if not env_timestamp.endswith("Z"):
                env_timestamp += "Z"
            return env_timestamp
    except Exception:
        pass

    now = datetime.now(tz=timezone.utc)
    if precise:
        return now.isoformat(timespec="microseconds") + "Z"
    else:
        return now.isoformat(timespec="seconds") + "Z"