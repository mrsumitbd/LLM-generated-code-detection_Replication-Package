from datetime import datetime, timedelta

class RateLimitTracker:
    """Track API rate limiting."""

    def __init__(self, limit: int, reset_interval: timedelta):
        self.limit = limit
        self.reset_interval = reset_interval
        self.requests = []
        self.last_reset_time = datetime.now()

    def can_make_request(self) -> bool:
        self._cleanup_requests()
        return len(self.requests) < self.limit

    def record_request(self) -> None:
        self._cleanup_requests()
        self.requests.append(datetime.now())

    def time_until_reset(self) -> timedelta:
        next_reset_time = self.last_reset_time + self.reset_interval
        return max(timedelta(0), next_reset_time - datetime.now())

    def _cleanup_requests(self):
        self.requests = [req for req in self.requests if req >= self.last_reset_time]