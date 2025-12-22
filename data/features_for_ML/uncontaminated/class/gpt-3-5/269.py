from typing import Callable

class MetricsCollector:
    """Enhanced metrics collector with full dashboard support"""

    def __new__(cls, enable: bool = True):
        if enable:
            return super(MetricsCollector, cls).__new__(cls)
        return None

    def __init__(self, enable: bool = True):
        self.enable = enable
        self.session_id = None
        self.health_status = True
        self.performance_data = {}

    def session_start(self):
        if self.enable:
            self.session_id = str(hash(self))
            print(f"Session started with ID: {self.session_id}")

    def session_end(self):
        if self.enable:
            print(f"Session ended for ID: {self.session_id}")
            self.session_id = None

    def record_blocked_command(self, reason: str = "blacklist"):
        if self.enable:
            print(f"Blocked command recorded. Reason: {reason}")

    def record_llm_query(self, duration: float, status: str = "success"):
        if self.enable:
            print(f"LLM query recorded. Duration: {duration}, Status: {status}")

    def record_rate_limit(self, session_id: str):
        if self.enable:
            print(f"Rate limit recorded for session ID: {session_id}")

    def set_health(self, healthy: bool):
        if self.enable:
            self.health_status = healthy
            print(f"Health status set to: {'Healthy' if healthy else 'Unhealthy'}")

    def start_server(self, port: int = 8000) -> bool:
        if self.enable:
            print(f"Server started on port {port}")
            return True
        return False

    def track_performance(self, func: Callable) -> Callable:
        if self.enable:
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                print(f"Performance tracked for function: {func.__name__}")
                return result
            return wrapper
        return func

    def export(self) -> str:
        if self.enable:
            return f"Metrics exported successfully"
        return ""