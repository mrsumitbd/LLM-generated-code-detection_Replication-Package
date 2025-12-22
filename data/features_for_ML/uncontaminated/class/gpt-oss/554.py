class CacheManager:
    """Class to handle cache management operations"""

    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.cache = {}
        self.deployment_status = {}
        self.update_cache_settings()

    def update_cache_settings(self):
        """Update cache configuration based on settings_manager."""
        # Example: set maximum cache size
        self.max_size = getattr(self.settings_manager, "cache_max_size", None)
        # Evict items if cache exceeds the new maximum size
        if self.max_size is not None and len(self.cache) > self.max_size:
            # Simple eviction: remove oldest entries
            keys_to_remove = list(self.cache.keys())[: len(self.cache) - self.max_size]
            for key in keys_to_remove:
                self.cache.pop(key, None)

    def get_cache_stats(self):
        """Return basic statistics about the cache."""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "keys": list(self.cache.keys()),
        }

    def clear_cache(self):
        """Clear all entries from the cache."""
        self.cache.clear()

    def get_deployment_status(self, domain):
        """Retrieve the deployment status for a given domain."""
        return self.deployment_status.get(domain)

    def set_deployment_status(self, domain, status):
        """Set the deployment status for a given domain."""
        self.deployment_status[domain] = status

    def remove_from_cache(self, domain):
        """Remove a specific domain from the cache."""
        self.cache.pop(domain, None)

    def get_cache_instance(self):
        """Return the underlying cache instance."""
        return self.cache