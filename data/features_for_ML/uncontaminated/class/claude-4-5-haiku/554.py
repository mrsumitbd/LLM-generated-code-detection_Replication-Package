class CacheManager:
    """Class to handle cache management operations"""

    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.cache = {}
        self.deployment_status = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'total_items': 0
        }

    def update_cache_settings(self):
        """Update cache settings from settings manager"""
        if self.settings_manager:
            cache_config = self.settings_manager.get_cache_settings()
            if cache_config:
                self.cache_stats['max_size'] = cache_config.get('max_size', 1000)
                self.cache_stats['ttl'] = cache_config.get('ttl', 3600)
                return True
        return False

    def get_cache_stats(self):
        """Get current cache statistics"""
        return {
            'hits': self.cache_stats.get('hits', 0),
            'misses': self.cache_stats.get('misses', 0),
            'total_items': len(self.cache),
            'max_size': self.cache_stats.get('max_size', 1000),
            'ttl': self.cache_stats.get('ttl', 3600)
        }

    def clear_cache(self):
        """Clear all cache entries"""
        self.cache.clear()
        self.deployment_status.clear()
        self.cache_stats['hits'] = 0
        self.cache_stats['misses'] = 0
        return True

    def get_deployment_status(self, domain):
        """Get deployment status for a specific domain"""
        if domain in self.deployment_status:
            self.cache_stats['hits'] = self.cache_stats.get('hits', 0) + 1
            return self.deployment_status[domain]
        else:
            self.cache_stats['misses'] = self.cache_stats.get('misses', 0) + 1
            return None

    def set_deployment_status(self, domain, status):
        """Set deployment status for a specific domain"""
        self.deployment_status[domain] = status
        self.cache_stats['total_items'] = len(self.cache) + len(self.deployment_status)
        return True

    def remove_from_cache(self, domain):
        """Remove a domain from cache"""
        if domain in self.cache:
            del self.cache[domain]
        if domain in self.deployment_status:
            del self.deployment_status[domain]
        self.cache_stats['total_items'] = len(self.cache) + len(self.deployment_status)
        return True

    def get_cache_instance(self):
        """Get the cache instance"""
        return {
            'cache': self.cache,
            'deployment_status': self.deployment_status,
            'stats': self.get_cache_stats()
        }