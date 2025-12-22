from typing import Tuple, Optional, Dict

class IPRateLimiter:
    """Simple IP-based rate limiter for preventing abuse without authentication"""

    def __init__(self):
        self.requests = {}
        self.window_size = 60  # in seconds
        self.max_requests = 10

    def is_allowed(self, client_ip: str, endpoint_type: str = 'default') -> Tuple[bool, Optional[str]]:
        current_time = time.time()
        self._cleanup_if_needed(current_time)

        key = f"{client_ip}_{endpoint_type}"
        if key not in self.requests:
            self.requests[key] = []

        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(current_time)
            return True, None
        else:
            return False, "Rate limit exceeded"

    def _cleanup_if_needed(self, current_time: float):
        for key in list(self.requests.keys()):
            self.requests[key] = [req_time for req_time in self.requests[key] if req_time > current_time - self.window_size]

            if not self.requests[key]:
                del self.requests[key]

    def get_stats(self) -> Dict:
        return {key: len(self.requests[key]) for key in self.requests}