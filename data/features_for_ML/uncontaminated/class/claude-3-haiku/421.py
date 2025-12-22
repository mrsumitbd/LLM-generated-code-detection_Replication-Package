from datetime import datetime, timedelta

class RateLimitTracker:
    """Track API rate limiting."""

    def __init__(self, max_requests: int, reset_time: timedelta):
        self.max_requests = max_requests
        self.reset_time = reset_time
        self.request_count = 0
        self.last_request_time = None

    def can_make_request(self) -> bool:
        if self.request_count < self.max_requests:
            return True
        elif self.last_request_time is None or datetime.now() - self.last_request_time >= self.reset_time:
            self.request_count = 1
            self.last_request_time = datetime.now()
            return True
        else:
            return False

    def record_request(self) -> None:
        self.request_count += 1
        self.last_request_time = datetime.now()

    def time_until_reset(self) -> timedelta:
        if self.last_request_time is None or self.request_count < self.max_requests:
            return timedelta(0)
        else:
            return self.reset_time - (datetime.now() - self.last_request_time)