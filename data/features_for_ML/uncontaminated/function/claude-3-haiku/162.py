def _get_backend() -> MemoryBackend:
    try:
        import redis
        return RedisBackend()
    except ImportError:
        try:
            import memcached
            return MemcachedBackend()
        except ImportError:
            return DictBackend()