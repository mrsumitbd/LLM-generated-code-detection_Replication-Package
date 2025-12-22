from collections import defaultdict
from time import time

class _MinimalRateLimiter:
    def __init__(self):
        self.rate_limits = defaultdict(dict)

    def enforce_rate_limit(self, key):
        for endpoint, config in self.rate_limits[key].items():
            last_request_time = config.get('last_request_time', 0)
            requests_in_window = config.get('requests_in_window', 0)
            window_duration = config['window_duration']
            max_requests = config['max_requests']

            current_time = time()
            if current_time - last_request_time <= window_duration:
                requests_in_window += 1
            else:
                requests_in_window = 1

            if requests_in_window > max_requests:
                return False

            self.rate_limits[key][endpoint] = {
                'last_request_time': current_time,
                'requests_in_window': requests_in_window,
                'window_duration': window_duration,
                'max_requests': max_requests
            }

        return True

    def configure_endpoint(self, name, config):
        for key in config:
            self.rate_limits[key][name] = config[key]