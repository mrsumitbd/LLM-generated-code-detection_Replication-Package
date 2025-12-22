class RateLimitConfig:
    def __init__(self, **kwargs):
        self.requests_per_second = kwargs.get('requests_per_second', 10)
        self.burst_size = kwargs.get('burst_size', 20)
        self.enabled = kwargs.get('enabled', True)
        self.timeout = kwargs.get('timeout', 60)
        self.retry_after = kwargs.get('retry_after', 1)
        self.max_retries = kwargs.get('max_retries', 3)
        
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)