class _MinimalRateLimiter:
    def __init__(self):
        self.configs = {}
        self.request_counts = {}
        self.last_reset_time = {}

    def enforce_rate_limit(self, key):
        import time
        
        if key not in self.configs:
            return True
        
        config = self.configs[key]
        current_time = time.time()
        
        if key not in self.request_counts:
            self.request_counts[key] = 0
            self.last_reset_time[key] = current_time
        
        time_elapsed = current_time - self.last_reset_time[key]
        window = config.get('window', 60)
        
        if time_elapsed >= window:
            self.request_counts[key] = 0
            self.last_reset_time[key] = current_time
        
        max_requests = config.get('max_requests', float('inf'))
        
        if self.request_counts[key] < max_requests:
            self.request_counts[key] += 1
            return True
        
        return False

    def configure_endpoint(self, name, config):
        self.configs[name] = config
        self.request_counts[name] = 0
        self.last_reset_time[name] = 0