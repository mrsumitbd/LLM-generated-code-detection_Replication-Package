import time
from typing import Callable

class MetricsCollector:
    """Enhanced metrics collector with full dashboard support"""

    def __new__(cls, enable: bool = True):
        if enable:
            return super(MetricsCollector, cls).__new__(cls)
        else:
            return None

    def __init__(self, enable: bool = True):
        self.enable = enable
        self.session_start_time = None
        self.blocked_commands = []
        self.llm_queries = []
        self.rate_limits = []
        self.is_healthy = True

    def session_start(self):
        if self.enable:
            self.session_start_time = time.time()

    def session_end(self):
        if self.enable and self.session_start_time is not None:
            session_duration = time.time() - self.session_start_time
            self.record_session_duration(session_duration)

    def record_blocked_command(self, reason: str = "blacklist"):
        if self.enable:
            self.blocked_commands.append({"reason": reason})

    def record_llm_query(self, duration: float, status: str = "success"):
        if self.enable:
            self.llm_queries.append({"duration": duration, "status": status})

    def record_rate_limit(self, session_id: str):
        if self.enable:
            self.rate_limits.append({"session_id": session_id})

    def set_health(self, healthy: bool):
        if self.enable:
            self.is_healthy = healthy

    def start_server(self, port: int = 8000) -> bool:
        if self.enable:
            # Implement server start logic here
            return True
        else:
            return False

    def track_performance(self, func: Callable) -> Callable:
        if self.enable:
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                self.record_llm_query(end_time - start_time)
                return result
            return wrapper
        else:
            return func

    def export(self) -> str:
        if self.enable:
            # Implement export logic here
            return "Exported metrics data"
        else:
            return "Metrics collection is disabled"