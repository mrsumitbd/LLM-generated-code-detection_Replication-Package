import time
from collections import defaultdict

class _MinimalRateLimiter:
    """
    A very small in‑memory rate limiter.

    Each endpoint can be configured with a maximum number of requests
    allowed in a given period (seconds).  The limiter keeps a timestamp
    list per endpoint and rejects any request that would exceed the
    configured limit.
    """

    def __init__(self):
        # endpoint name -> config dict (must contain 'max_requests' and 'period')
        self._configs = {}
        # endpoint name -> list of request timestamps
        self._state = defaultdict(list)

    def configure_endpoint(self, name, config):
        """
        Register or update the rate‑limit configuration for an endpoint.

        Parameters
        ----------
        name : str
            Identifier for the endpoint.
        config : dict
            Must contain:
                - 'max_requests': int, maximum allowed requests in the period.
                - 'period': float, time window in seconds.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dict")
        if 'max_requests' not in config or 'period' not in config:
            raise ValueError("config must contain 'max_requests' and 'period'")
        if not isinstance(config['max_requests'], int) or config['max_requests'] <= 0:
            raise ValueError("'max_requests' must be a positive integer")
        if not isinstance(config['period'], (int, float)) or config['period'] <= 0:
            raise ValueError("'period' must be a positive number")
        self._configs[name] = {
            'max_requests': int(config['max_requests']),
            'period': float(config['period'])
        }
        # Ensure state list exists
        self._state[name]  # accessed to create entry

    def enforce_rate_limit(self, key):
        """
        Check whether a request for the given endpoint key is allowed.

        Parameters
        ----------
        key : str
            The endpoint name to check.

        Returns
        -------
        bool
            True if the request is allowed.

        Raises
        ------
        KeyError
            If the endpoint has not been configured.
        RuntimeError
            If the request would exceed the configured rate limit.
        """
        if key not in self._configs:
            raise KeyError(f"Endpoint '{key}' is not configured")

        config = self._configs[key]
        max_requests = config['max_requests']
        period = config['period']

        now = time.time()
        timestamps = self._state[key]

        # Remove timestamps older than the period window
        window_start = now - period
        while timestamps and timestamps[0] < window_start:
            timestamps.pop(0)

        if len(timestamps) >= max_requests:
            raise RuntimeError(f"Rate limit exceeded for endpoint '{key}'")

        timestamps.append(now)
        return True