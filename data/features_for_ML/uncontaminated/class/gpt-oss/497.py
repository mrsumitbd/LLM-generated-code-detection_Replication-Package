from __future__ import annotations

import hashlib
import time
from typing import Any, Dict, List, Optional


class ToolExecutor:
    """独立的工具执行器组件

    可以直接输入聊天消息内容，自动判断并执行相应的工具，返回结构化的工具执行结果。
    """

    def __init__(self, chat_id: str, enable_cache: bool = True, cache_ttl: int = 3):
        self.chat_id = chat_id
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl  # seconds
        self._cache: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}

    def _get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        返回可用工具的定义列表。这里返回空列表，实际使用时可根据业务自行实现。
        """
        return []

    def _generate_cache_key(self, target_message: str, chat_history: str, sender: str) -> str:
        """
        生成缓存键，使用 SHA256 对三部分内容进行哈希。
        """
        key_str = f"{self.chat_id}|{sender}|{target_message}|{chat_history}"
        return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """
        从缓存中获取结果，如果缓存已过期则返回 None。
        """
        if not self.enable_cache:
            return None

        entry = self._cache.get(cache_key)
        if entry is None:
            return None

        timestamp, result = entry
        if time.time() - timestamp > self.cache_ttl:
            # 过期，删除
            del self._cache[cache_key]
            return None

        return result

    def _set_cache(self, cache_key: str, result: List[Dict[str, Any]]):
        """
        将结果写入缓存。
        """
        if not self.enable_cache:
            return
        self._cache[cache_key] = (time.time(), result)
        self._cleanup_expired_cache()

    def _cleanup_expired_cache(self):
        """
        清理所有已过期的缓存条目。
        """
        if not self.enable_cache:
            return
        now = time.time()
        keys_to_delete = [
            key for key, (ts, _) in self._cache.items() if now - ts > self.cache_ttl
        ]
        for key in keys_to_delete:
            del self._cache[key]

    def clear_cache(self):
        """清空整个缓存。"""
        self._cache.clear()

    def get_cache_status(self) -> Dict[str, Any]:
        """返回缓存状态信息。"""
        self._cleanup_expired_cache()
        return {
            "enabled": self.enable_cache,
            "ttl_seconds": self.cache_ttl,
            "entries": len(self._cache),
            "keys": list(self._cache.keys()),
        }

    def set_cache_config(self, enable_cache: Optional[bool] = None, cache_ttl: int = -1):
        """
        动态修改缓存配置。
        """
        if enable_cache is not None:
            self.enable_cache = enable_cache
        if cache_ttl > 0:
            self.cache_ttl = cache_ttl
        # 如果禁用缓存，立即清空
        if not self.enable_cache:
            self.clear_cache()