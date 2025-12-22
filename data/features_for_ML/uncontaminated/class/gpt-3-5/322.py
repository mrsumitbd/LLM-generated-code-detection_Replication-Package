class ResponseCache:
    """Simple TTL-based cache for API responses."""

    def __init__(self):
        self.cache = {}
        self.ttl_mapping = {
            '/endpoint1': 60,
            '/endpoint2': 120,
            '/endpoint3': 180
        }

    def _get_cache_key(self, endpoint: str) -> str:
        return endpoint

    def _get_ttl_for_endpoint(self, endpoint: str) -> int:
        return self.ttl_mapping.get(endpoint, 0)

    def get_stats(self) -> Dict[str, Any]:
        return {
            'cache_size': len(self.cache),
            'ttl_mapping': self.ttl_mapping
        }