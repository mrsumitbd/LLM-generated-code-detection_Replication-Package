import time

class CacheManager:
    """Class to handle cache management operations"""

    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
        self.cache_ttl = self.settings_manager.get_cache_ttl()

    def update_cache_settings(self):
        self.cache_ttl = self.settings_manager.get_cache_ttl()

    def get_cache_stats(self):
        return self.cache_stats

    def clear_cache(self):
        self.cache.clear()
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }

    def get_deployment_status(self, domain):
        if domain in self.cache:
            self.cache_stats["hits"] += 1
            return self.cache[domain]["status"]
        else:
            self.cache_stats["misses"] += 1
            status = self.settings_manager.get_deployment_status(domain)
            self.cache[domain] = {
                "status": status,
                "timestamp": time.time()
            }
            return status

    def set_deployment_status(self, domain, status):
        self.cache[domain] = {
            "status": status,
            "timestamp": time.time()
        }
        self.settings_manager.set_deployment_status(domain, status)

    def remove_from_cache(self, domain):
        if domain in self.cache:
            del self.cache[domain]
            self.cache_stats["evictions"] += 1

    def get_cache_instance(self):
        return self.cache