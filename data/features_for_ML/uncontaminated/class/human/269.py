from functools import wraps
import asyncio
import time
from typing import Optional, Callable, Dict, Any
from threading import Lock
from prometheus_client import Counter, Gauge, Histogram, start_http_server, REGISTRY
from prometheus_client import generate_latest

class MetricsCollector:
    """Enhanced metrics collector with full dashboard support"""

    _instance = None
    _lock = Lock()

    def __new__(cls, enable: bool = True):
        """Singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, enable: bool = True):
        if self._initialized:
            return

        self.enabled = enable and PROMETHEUS_AVAILABLE
        self._server_started = False
        self._initialized = True

        if not self.enabled:
            return

        # === COMMAND METRICS (from @perf decorator) ===
        self.function_calls = Counter(
            "copilot_commands_total", "Total function calls", ["function", "status"]
        )
        self.function_duration = Histogram(
            "copilot_command_seconds",
            "Function execution duration",
            ["function", "type"],
        )

        # === SESSION METRICS ===
        self.active_sessions = Gauge(
            "copilot_sessions_active", "Number of currently active sessions"
        )

        # === BLOCKED COMMANDS ===
        self.blocked_commands = Counter(
            "copilot_blocked_total", "Total blocked/rejected commands", ["reason"]
        )

        # === LLM QUERY METRICS ===
        self.llm_queries = Counter(
            "copilot_queries_total", "Total LLM queries", ["status"]
        )
        self.llm_query_duration = Histogram(
            "copilot_query_seconds",
            "LLM query duration in seconds",
            ["status"],
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0),
        )

        # === RATE LIMITING ===
        self.rate_limited = Counter(
            "copilot_rate_limited_total", "Total rate limited requests", ["session_id"]
        )

        # === SYSTEM HEALTH ===
        self.health_status = Gauge(
            "copilot_health_status", "Overall health status (1=healthy, 0=unhealthy)"
        )
        self.health_status.set(1)

    # === SESSION MANAGEMENT ===
    def session_start(self):
        """Increment active sessions counter"""
        if self.enabled:
            self.active_sessions.inc()

    def session_end(self):
        """Decrement active sessions counter"""
        if self.enabled:
            self.active_sessions.dec()

    # === BLOCKED COMMANDS ===
    def record_blocked_command(self, reason: str = "blacklist"):
        """Record a blocked command attempt"""
        if self.enabled:
            self.blocked_commands.labels(reason=reason).inc()

    # === LLM QUERIES ===
    def record_llm_query(self, duration: float, status: str = "success"):
        """
        Record LLM query with duration

        Args:
            duration: Query duration in seconds
            status: Query status (success, error, timeout)
        """
        if self.enabled:
            self.llm_queries.labels(status=status).inc()
            self.llm_query_duration.labels(status=status).observe(duration)

    # === RATE LIMITING ===
    def record_rate_limit(self, session_id: str):
        """Record a rate limit hit"""
        if self.enabled:
            self.rate_limited.labels(session_id=session_id).inc()

    # === HEALTH ===
    def set_health(self, healthy: bool):
        """Set overall health status"""
        if self.enabled:
            self.health_status.set(1 if healthy else 0)

    # === SERVER MANAGEMENT ===
    def start_server(self, port: int = 8000) -> bool:
        """
        Start Prometheus metrics HTTP server

        Returns:
            True if server started, False if already running or disabled
        """
        if not self.enabled or self._server_started:
            return False

        try:
            start_http_server(port, addr="0.0.0.0")
            self._server_started = True
            return True
        except OSError:
            return False

    # === PERFORMANCE DECORATOR ===
    def track_performance(self, func: Callable) -> Callable:
        """
        Decorator to track function performance
        Works with both sync and async functions
        """

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not self.enabled:
                return func(*args, **kwargs)

            start = time.time()
            status = "success"
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                raise
            finally:
                duration = time.time() - start
                self.function_calls.labels(function=func.__name__, status=status).inc()
                self.function_duration.labels(
                    function=func.__name__, type="command"
                ).observe(duration)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not self.enabled:
                return await func(*args, **kwargs)

            start = time.time()
            status = "success"
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = "error"
                raise
            finally:
                duration = time.time() - start
                self.function_calls.labels(function=func.__name__, status=status).inc()
                self.function_duration.labels(
                    function=func.__name__, type="command"
                ).observe(duration)

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    # === EXPORT ===
    def export(self) -> str:
        """Export metrics in Prometheus format"""
        if not self.enabled:
            return "Metrics disabled"

        from prometheus_client import generate_latest

        return generate_latest(REGISTRY).decode("utf-8")