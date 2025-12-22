from typing import Tuple, Optional, Dict, List
import time
import threading


class IPRateLimiter:
    """Simple IP-based rate limiter for preventing abuse without authentication"""

    # Rate‑limit configuration
    WINDOW_SECONDS: int = 60          # Sliding window length in seconds
    MAX_REQUESTS: int = 10            # Max requests allowed per IP per endpoint in the window

    def __init__(self):
        # Structure: {ip: {endpoint: [timestamp, ...]}}
        self._data: Dict[str, Dict[str, List[float]]] = {}
        self._lock = threading.Lock()
        self._last_cleanup: float = time.time()

    def is_allowed(self, client_ip: str, endpoint_type: str = 'default') -> Tuple[bool, Optional[str]]:
        """
        Check if a request from `client_ip` to `endpoint_type` is allowed.
        Returns a tuple (allowed, reason). If allowed is True, reason is None.
        """
        now = time.time()
        with self._lock:
            self._cleanup_if_needed(now)

            ip_map = self._data.setdefault(client_ip, {})
            timestamps = ip_map.setdefault(endpoint_type, [])

            # Remove timestamps older than the window
            cutoff = now - self.WINDOW_SECONDS
            while timestamps and timestamps[0] < cutoff:
                timestamps.pop(0)

            if len(timestamps) >= self.MAX_REQUESTS:
                return False, f"Rate limit exceeded: {self.MAX_REQUESTS} requests per {self.WINDOW_SECONDS}s"

            timestamps.append(now)
            return True, None

    def _cleanup_if_needed(self, current_time: float):
        """
        Periodically clean up old timestamps from all IPs to keep memory usage bounded.
        """
        if current_time - self._last_cleanup < self.WINDOW_SECONDS:
            return  # Not time to clean up yet

        cutoff = current_time - self.WINDOW_SECONDS
        for ip, endpoints in list(self._data.items()):
            for ep, timestamps in list(endpoints.items()):
                # Remove old timestamps
                while timestamps and timestamps[0] < cutoff:
                    timestamps.pop(0)
                if not timestamps:
                    del endpoints[ep]
            if not endpoints:
                del self._data[ip]

        self._last_cleanup = current_time

    def get_stats(self) -> Dict:
        """
        Return a snapshot of current request counts per IP and endpoint.
        """
        with self._lock:
            now = time.time()
            cutoff = now - self.WINDOW_SECONDS
            stats: Dict[str, Dict[str, int]] = {}
            for ip, endpoints in self._data.items():
                ep_stats: Dict[str, int] = {}
                for ep, timestamps in endpoints.items():
                    # Count only recent timestamps
                    count = sum(1 for ts in timestamps if ts >= cutoff)
                    if count > 0:
                        ep_stats[ep] = count
                if ep_stats:
                    stats[ip] = ep_stats
            return stats