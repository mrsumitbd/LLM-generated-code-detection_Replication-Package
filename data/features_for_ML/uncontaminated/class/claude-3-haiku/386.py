class RateLimitConfig:
    def __init__(self, **kwargs):
        self.max_requests = kwargs.get('max_requests', 100)
        self.time_window = kwargs.get('time_window', 60)
        self.enabled = kwargs.get('enabled', True)
        self.error_message = kwargs.get('error_message', 'Rate limit exceeded')
        self.headers = kwargs.get('headers', {'X-RateLimit-Limit': self.max_requests,
                                             'X-RateLimit-Remaining': self.max_requests,
                                             'X-RateLimit-Reset': self.time_window})