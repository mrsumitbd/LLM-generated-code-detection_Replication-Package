from typing import Tuple, Optional, Dict
from collections import defaultdict
from time import time

class IPRateLimiter:
    """Simple IP-based rate limiter for preventing abuse without authentication"""

    def __init__(self):
        self.request_counts = defaultdict(lambda: defaultdict(int))
        self.request_timestamps = defaultdict(lambda: defaultdict(list))
        self.max_requests = 10
        self.time_window = 60  # 1 minute

    def is_allowed(self, client_ip: str, endpoint_type: str = 'default') -> Tuple[bool, Optional[str]]:
        self._cleanup_if_needed(time())
        request_count = self.request_counts[client_ip][endpoint_type]
        if request_count < self.max_requests:
            self.request_counts[client_ip][endpoint_type] += 1
            self.request_timestamps[client_ip][endpoint_type].append(time())
            return True, None
        else:
            return False, f"Rate limit exceeded for IP {client_ip} on endpoint {endpoint_type}"

    def _cleanup_if_needed(self, current_time: float):
        for client_ip, endpoints in self.request_timestamps.items():
            for endpoint_type, timestamps in endpoints.items():
                while timestamps and current_time - timestamps[0] > self.time_window:
                    timestamps.pop(0)
                    self.request_counts[client_ip][endpoint_type] -= 1

    def get_stats(self) -> Dict:
        return {
            "request_counts": self.request_counts,
            "request_timestamps": self.request_timestamps,
            "max_requests": self.max_requests,
            "time_window": self.time_window
        }