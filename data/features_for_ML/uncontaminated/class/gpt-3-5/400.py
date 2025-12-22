class _MinimalRateLimiter:
    
    def __init__(self):
        self.rate_limits = {}

    def enforce_rate_limit(self, key):
        if key in self.rate_limits:
            # Implement rate limiting logic here
            pass
        else:
            raise KeyError(f"Rate limit configuration not found for key: {key}")

    def configure_endpoint(self, name, config):
        self.rate_limits[name] = config