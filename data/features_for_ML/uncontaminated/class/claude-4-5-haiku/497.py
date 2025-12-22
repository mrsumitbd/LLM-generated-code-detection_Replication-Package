class ToolExecutor:
    """独立的工具执行器组件

    可以直接输入聊天消息内容，自动判断并执行相应的工具，返回结构化的工具执行结果。
    """

    def __init__(self, chat_id: str, enable_cache: bool = True, cache_ttl: int = 3):
        self.chat_id = chat_id
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self._cache = {}
        self._cache_timestamps = {}

    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Search for information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]

    def _generate_cache_key(self, target_message: str, chat_history: str, sender: str) -> str:
        import hashlib
        content = f"{self.chat_id}:{target_message}:{chat_history}:{sender}"
        return hashlib.md5(content.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[List[Dict]]:
        if not self.enable_cache or cache_key not in self._cache:
            return None
        
        import time
        timestamp = self._cache_timestamps.get(cache_key)
        if timestamp and time.time() - timestamp > self.cache_ttl * 60:
            del self._cache[cache_key]
            del self._cache_timestamps[cache_key]
            return None
        
        return self._cache.get(cache_key)

    def _set_cache(self, cache_key: str, result: List[Dict]):
        if not self.enable_cache:
            return
        
        import time
        self._cache[cache_key] = result
        self._cache_timestamps[cache_key] = time.time()

    def _cleanup_expired_cache(self):
        import time
        current_time = time.time()
        expired_keys = [
            key for key, timestamp in self._cache_timestamps.items()
            if current_time - timestamp > self.cache_ttl * 60
        ]
        for key in expired_keys:
            del self._cache[key]
            del self._cache_timestamps[key]

    def clear_cache(self):
        self._cache.clear()
        self._cache_timestamps.clear()

    def get_cache_status(self) -> Dict:
        self._cleanup_expired_cache()
        return {
            "chat_id": self.chat_id,
            "enable_cache": self.enable_cache,
            "cache_ttl": self.cache_ttl,
            "cache_size": len(self._cache),
            "cached_keys": list(self._cache.keys())
        }

    def set_cache_config(self, enable_cache: Optional[bool] = None, cache_ttl: int = -1):
        if enable_cache is not None:
            self.enable_cache = enable_cache
        if cache_ttl > 0:
            self.cache_ttl = cache_ttl