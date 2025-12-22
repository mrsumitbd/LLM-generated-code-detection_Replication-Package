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
        # 1. Check environment variable
        env_val = os.getenv(env_var)
        if env_val is not None:
            val = env_val.strip()
            # Normalize '+00:00' to 'Z'
            if val.endswith("+00:00"):
                val = val[:-6] + "Z"
            # If no timezone indicator, append 'Z'
            if not (val.endswith("Z") or "+" in val or "-" in val):
                val += "Z"
            return val

        # 2. Generate current UTC timestamp
        now = datetime.now(timezone.utc)
        if not precise:
            now = now.replace(microsecond=0)
        ts = now.isoformat(timespec="microseconds" if precise else "seconds")
        # Replace '+00:00' with 'Z'
        if ts.endswith("+00:00"):
            ts = ts[:-6] + "Z"
        return ts

    except Exception:
        # 3. Fallback on any error
        return fallback