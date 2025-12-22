from typing import Tuple, Optional, Dict
from collections import defaultdict
import time

class IPRateLimiter:
    """Simple IP-based rate limiter for preventing abuse without authentication"""

    def __init__(self):
        self.requests = defaultdict(list)  # IP -> list of request timestamps
        self.blocked_ips = {}  # IP -> unblock time
        self.stats = defaultdict(lambda: {'allowed': 0, 'blocked': 0})
        self.last_cleanup = time.time()
        
        # Rate limit configurations per endpoint type
        self.limits = {
            'default': {'requests': 100, 'window': 60},
            'login': {'requests': 5, 'window': 300},
            'api': {'requests': 1000, 'window': 3600},
            'upload': {'requests': 10, 'window': 3600}
        }
        self.block_duration = 3600  # 1 hour block
        self.cleanup_interval = 300  # Cleanup every 5 minutes

    def is_allowed(self, client_ip: str, endpoint_type: str = 'default') -> Tuple[bool, Optional[str]]:
        current_time = time.time()
        self._cleanup_if_needed(current_time)
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            if current_time < self.blocked_ips[client_ip]:
                self.stats[client_ip]['blocked'] += 1
                return False, f"IP blocked until {self.blocked_ips[client_ip]}"
            else:
                del self.blocked_ips[client_ip]
        
        # Get rate limit config for endpoint type
        limit_config = self.limits.get(endpoint_type, self.limits['default'])
        max_requests = limit_config['requests']
        window = limit_config['window']
        
        # Remove old requests outside the window
        cutoff_time = current_time - window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > cutoff_time
        ]
        
        # Check if limit exceeded
        if len(self.requests[client_ip]) >= max_requests:
            self.blocked_ips[client_ip] = current_time + self.block_duration
            self.stats[client_ip]['blocked'] += 1
            return False, f"Rate limit exceeded for {endpoint_type}. Blocked for {self.block_duration}s"
        
        # Allow request
        self.requests[client_ip].append(current_time)
        self.stats[client_ip]['allowed'] += 1
        return True, None

    def _cleanup_if_needed(self, current_time: float):
        if current_time - self.last_cleanup > self.cleanup_interval:
            # Remove expired blocks
            expired_ips = [
                ip for ip, unblock_time in self.blocked_ips.items()
                if current_time >= unblock_time
            ]
            for ip in expired_ips:
                del self.blocked_ips[ip]
            
            # Remove old request records
            cutoff_time = current_time - max(
                config['window'] for config in self.limits.values()
            )
            ips_to_clean = []
            for ip, timestamps in self.requests.items():
                self.requests[ip] = [
                    ts for ts in timestamps if ts > cutoff_time
                ]
                if not self.requests[ip]:
                    ips_to_clean.append(ip)
            
            for ip in ips_to_clean:
                del self.requests[ip]
            
            self.last_cleanup = current_time

    def get_stats(self) -> Dict:
        return {
            'total_ips_tracked': len(self.requests),
            'blocked_ips': len(self.blocked_ips),
            'per_ip_stats': dict(self.stats),
            'limits': self.limits,
            'block_duration': self.block_duration
        }