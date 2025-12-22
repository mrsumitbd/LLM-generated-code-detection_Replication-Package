import threading
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple


class UniversalMessageSender:
    """管理消息的注册、即时处理、发送和存储，并跟踪思考状态。"""

    def __init__(self):
        # 记录消息类型到处理函数的映射
        self._handlers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)
        # 存储已接收或已发送的消息
        self._message_log: List[Tuple[datetime, str, Any]] = []
        # 思考状态（True 表示正在思考）
        self._thinking: bool = False
        # 线程安全锁
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # 注册与管理处理器
    # ------------------------------------------------------------------
    def register_handler(self, msg_type: str, handler: Callable[[Any], None]) -> None:
        """为指定消息类型注册处理函数。"""
        if not callable(handler):
            raise TypeError("handler 必须是可调用对象")
        with self._lock:
            self._handlers[msg_type].append(handler)

    def unregister_handler(self, msg_type: str, handler: Callable[[Any], None]) -> None:
        """移除指定消息类型的处理函数。"""
        with self._lock:
            if handler in self._handlers.get(msg_type, []):
                self._handlers[msg_type].remove(handler)
                if not self._handlers[msg_type]:
                    del self._handlers[msg_type]

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process_message(self, msg_type: str, payload: Any) -> None:
        """立即处理消息，调用所有注册的处理器。"""
        handlers = []
        with self._lock:
            handlers = list(self._handlers.get(msg_type, []))
        for handler in handlers:
            try:
                handler(payload)
            except Exception as e:
                # 记录错误但不阻止其他处理器
                self._log_error(f"处理器 {handler} 抛出异常: {e}")

    # ------------------------------------------------------------------
    # 发送与存储
    # ------------------------------------------------------------------
    def send_message(self, msg_type: str, payload: Any) -> None:
        """发送消息并记录。"""
        timestamp = datetime.utcnow()
        with self._lock:
            self._message_log.append((timestamp, msg_type, payload))
        # 发送后立即处理
        self.process_message(msg_type, payload)

    def store_message(self, msg_type: str, payload: Any) -> None:
        """仅存储消息，不立即处理。"""
        timestamp = datetime.utcnow()
        with self._lock:
            self._message_log.append((timestamp, msg_type, payload))

    # ------------------------------------------------------------------
    # 思考状态
    # ------------------------------------------------------------------
    def set_thinking(self, state: bool) -> None:
        """设置思考状态。"""
        with self._lock:
            self._thinking = state

    def is_thinking(self) -> bool:
        """返回当前思考状态。"""
        with self._lock:
            return self._thinking

    # ------------------------------------------------------------------
    # 日志与查询
    # ------------------------------------------------------------------
    def get_message_log(self) -> List[Tuple[datetime, str, Any]]:
        """返回完整的消息日志。"""
        with self._lock:
            return list(self._message_log)

    def get_messages_by_type(self, msg_type: str) -> List[Tuple[datetime, Any]]:
        """按消息类型过滤日志。"""
        with self._lock:
            return [(ts, payload) for ts, mt, payload in self._message_log if mt == msg_type]

    def _log_error(self, message: str) -> None:
        """内部错误日志，默认打印到标准错误。"""
        import sys
        print(f"[ERROR] {datetime.utcnow().isoformat()} - {message}", file=sys.stderr)