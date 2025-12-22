from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class RateLimitTracker:
    """Track API rate limiting."""
    
    max_requests: int
    window_seconds: int
    requests: list = field(default_factory=list)
    
    def __post_init__(self):
        self.requests = []
    
    def can_make_request(self) -> bool:
        now = datetime.now()
        cutoff_time = now - timedelta(seconds=self.window_seconds)
        
        self.requests = [req_time for req_time in self.requests if req_time > cutoff_time]
        
        return len(self.requests) < self.max_requests
    
    def record_request(self) -> None:
        self.requests.append(datetime.now())
    
    def time_until_reset(self) -> timedelta:
        if not self.requests:
            return timedelta(seconds=0)
        
        oldest_request = min(self.requests)
        reset_time = oldest_request + timedelta(seconds=self.window_seconds)
        now = datetime.now()
        
        time_remaining = reset_time - now
        
        if time_remaining.total_seconds() <= 0:
            return timedelta(seconds=0)
        
        return time_remaining