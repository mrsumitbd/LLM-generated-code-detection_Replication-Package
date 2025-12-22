from datetime import datetime, timedelta

class RateLimitTracker:
    """Track API rate limiting."""

    requests_per_window: int = 100
    window_seconds: int = 3600
    requests_made: int = 0
    window_start: datetime = None

    def __post_init__(self):
        if self.window_start is None:
            self.window_start = datetime.utcnow()

    def can_make_request(self) -> bool:
        """Check if we can make another request within rate limits."""
        now = datetime.utcnow()

        # Reset window if expired
        if now - self.window_start > timedelta(seconds=self.window_seconds):
            self.requests_made = 0
            self.window_start = now

        return self.requests_made < self.requests_per_window

    def record_request(self) -> None:
        """Record a successful API request."""
        self.requests_made += 1

    def time_until_reset(self) -> timedelta:
        """Get time until rate limit window resets."""
        window_end = self.window_start + timedelta(seconds=self.window_seconds)
        remaining = window_end - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)