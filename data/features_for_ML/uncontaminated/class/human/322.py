import asyncio
from typing import Any, Dict, Optional, Callable
import time
import json
import hashlib

class ResponseCache:
    """Simple TTL-based cache for API responses."""
    
    def __init__(self):
        self.cache: Dict[str, tuple[Any, float]] = {}
        self._lock = asyncio.Lock()
        
        # Default TTLs for different endpoint types (in seconds)
        self.default_ttls = {
            "leagues": 3600,      # 1 hour - leagues don't change often
            "teams": 1800,        # 30 minutes - team info fairly static
            "standings": 300,     # 5 minutes - standings update after games
            "roster": 300,        # 5 minutes - roster changes matter
            "matchup": 60,        # 1 minute - live scoring during games
            "players": 600,       # 10 minutes - free agents change slowly
            "draft": 86400,       # 24 hours - draft results are static
            "waiver": 300,        # 5 minutes - waiver wire is dynamic
            "user": 3600,         # 1 hour - user info rarely changes
        }
    
    def _get_cache_key(self, endpoint: str) -> str:
        """Generate cache key from endpoint."""
        return hashlib.md5(endpoint.encode()).hexdigest()
    
    def _get_ttl_for_endpoint(self, endpoint: str) -> int:
        """Determine TTL based on endpoint type."""
        # Check endpoint patterns to determine type
        if "leagues" in endpoint or "games" in endpoint:
            return self.default_ttls["leagues"]
        elif "standings" in endpoint:
            return self.default_ttls["standings"]
        elif "roster" in endpoint:
            return self.default_ttls["roster"]
        elif "matchup" in endpoint or "scoreboard" in endpoint:
            return self.default_ttls["matchup"]
        elif "players" in endpoint and "status=A" in endpoint:
            return self.default_ttls["players"]
        elif "draft" in endpoint:
            return self.default_ttls["draft"]
        elif "teams" in endpoint:
            return self.default_ttls["teams"]
        elif "users" in endpoint:
            return self.default_ttls["user"]
        else:
            return 300  # Default 5 minutes
    
    async def get(self, endpoint: str) -> Optional[Any]:
        """Get cached response if valid."""
        async with self._lock:
            cache_key = self._get_cache_key(endpoint)
            
            if cache_key in self.cache:
                data, timestamp = self.cache[cache_key]
                ttl = self._get_ttl_for_endpoint(endpoint)
                
                if time.time() - timestamp < ttl:
                    age = time.time() - timestamp
                    return data
                else:
                    # Expired, remove from cache
                    del self.cache[cache_key]
            
            return None
    
    async def set(self, endpoint: str, data: Any):
        """Store response in cache."""
        async with self._lock:
            cache_key = self._get_cache_key(endpoint)
            self.cache[cache_key] = (data, time.time())
    
    async def clear(self, pattern: Optional[str] = None):
        """Clear cache entries matching pattern or all if no pattern."""
        async with self._lock:
            if pattern:
                keys_to_delete = [
                    key for key in self.cache.keys()
                    if pattern in key
                ]
                for key in keys_to_delete:
                    del self.cache[key]
            else:
                self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        now = time.time()
        total_entries = len(self.cache)
        
        expired_count = 0
        total_size = 0
        
        for endpoint_hash, (data, timestamp) in self.cache.items():
            # Estimate size (rough)
            total_size += len(json.dumps(data, default=str))
            
            # Find endpoint type from hash (approximate)
            for endpoint_type in self.default_ttls:
                ttl = self.default_ttls[endpoint_type]
                if now - timestamp >= ttl:
                    expired_count += 1
                    break
        
        return {
            "total_entries": total_entries,
            "expired_entries": expired_count,
            "active_entries": total_entries - expired_count,
            "cache_size_bytes": total_size,
            "cache_size_mb": round(total_size / (1024 * 1024), 2)
        }