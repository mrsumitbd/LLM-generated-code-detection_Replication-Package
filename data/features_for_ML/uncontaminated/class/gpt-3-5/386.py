class RateLimitConfig:

    def __init__(self, **kwargs):
        self.limit = kwargs.get('limit', 100)
        self.interval = kwargs.get('interval', 60)
        self.method = kwargs.get('method', 'GET')
        self.endpoint = kwargs.get('endpoint', '/')
        self.enabled = kwargs.get('enabled', True)

    def __str__(self):
        return f"RateLimitConfig(limit={self.limit}, interval={self.interval}, method='{self.method}', endpoint='{self.endpoint}', enabled={self.enabled})"