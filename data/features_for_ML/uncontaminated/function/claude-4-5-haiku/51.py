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
    import os
    from datetime import datetime, timezone
    
    # Check if environment variable is set
    env_value = os.environ.get(env_var)
    if env_value is not None:
        # Validate and normalize the environment variable value
        # If it doesn't contain timezone info, append 'Z'
        if '+' not in env_value and '-' not in env_value.split('T')[-1] and not env_value.endswith('Z'):
            env_value = env_value + 'Z'
        return env_value
    
    try:
        # Generate current UTC timestamp
        now = datetime.now(timezone.utc)
        
        # Strip microseconds unless precise is True
        if not precise:
            now = now.replace(microsecond=0)
        
        # Format as ISO-8601 with 'Z' suffix
        timestamp = now.isoformat()
        
        # Normalize '+00:00' to 'Z'
        if timestamp.endswith('+00:00'):
            timestamp = timestamp[:-6] + 'Z'
        
        return timestamp
    except Exception:
        return fallback