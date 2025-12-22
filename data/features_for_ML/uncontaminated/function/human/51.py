from datetime import datetime, timezone
import os

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
        override = os.getenv(env_var)
        if override:
            # Basic normalization: ensure trailing Z if no timezone specified
            if override.endswith("Z") or override.endswith("z"):
                return override.rstrip("zZ") + "Z"
            if "+" in override or override.endswith("Z"):
                return override.replace("+00:00", "Z")
            return override + "Z"

        dt = datetime.now(timezone.utc)
        if not precise:
            dt = dt.replace(microsecond=0)
        return dt.isoformat().replace("+00:00", "Z")
    except Exception:
        return fallback