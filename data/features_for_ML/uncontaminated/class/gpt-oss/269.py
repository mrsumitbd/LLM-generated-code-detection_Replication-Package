import json
import time
import uuid
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import wraps
from typing import Callable, Dict, Any


class MetricsCollector:
    """Enhanced metrics collector with full dashboard support"""

    _instance = None

    def __new__(cls, enable: bool = True):
        if cls._instance is None:
            cls._instance = super(MetricsCollector, cls).__new__(cls)
        return cls._instance

    def __init__(self, enable: bool = True):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.enable = enable
        self._metrics: Dict[str, Any] = {
            "blocked_commands": 0,
            "llm_queries": {"success": 0, "failure": 0},
            "rate_limits": 0,
            "sessions": {},
            "health": True,
        }
        self._current_session: Dict[str, Any] | None = None
        self._server_thread: threading.Thread | None = None
        self._server: HTTPServer | None = None
        self._initialized = True

    def session_start(self):
        if not self.enable:
            return
        session_id = str(uuid.uuid4())
        self._current_session = {
            "id": session_id,
            "start": datetime.utcnow(),
            "commands_blocked": 0,
            "llm_queries": {"success": 0, "failure": 0},
            "rate_limits": 0,
        }
        self._metrics["sessions"][session_id] = self._current_session

    def session_end(self):
        if not self.enable or not self._current_session:
            return
        self._current_session["end"] = datetime.utcnow()
        self._current_session = None

    def record_blocked_command(self, reason: str = "blacklist"):
        if not self.enable:
            return
        self._metrics["blocked_commands"] += 1
        if self._current_session:
            self._current_session["commands_blocked"] += 1

    def record_llm_query(self, duration: float, status: str = "success"):
        if not self.enable:
            return
        if status not in ("success", "failure"):
            status = "failure"
        self._metrics["llm_queries"][status] += 1
        if self._current_session:
            self._current_session["llm_queries"][status] += 1

    def record_rate_limit(self, session_id: str):
        if not self.enable:
            return
        self._metrics["rate_limits"] += 1
        if session_id in self._metrics["sessions"]:
            self._metrics["sessions"][session_id]["rate_limits"] += 1

    def set_health(self, healthy: bool):
        if not self.enable:
            return
        self._metrics["health"] = healthy

    def start_server(self, port: int = 8000) -> bool:
        if not self.enable or self._server_thread:
            return False

        class MetricsHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path != "/metrics":
                    self.send_response(404)
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = json.dumps(self.server.collector.export_dict(), indent=2)
                self.wfile.write(response.encode())

            def log_message(self, format, *args):
                # Suppress default logging
                return

        server = HTTPServer(("0.0.0.0", port), MetricsHandler)
        server.collector = self

        def serve():
            try:
                server.serve_forever()
            except Exception:
                pass

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        self._server_thread = thread
        self._server = server
        return True

    def track_performance(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not self.enable:
                return func(*args, **kwargs)
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                self.record_llm_query(duration, status="success")
        return wrapper

    def export(self) -> str:
        return json.dumps(self.export_dict(), indent=2)

    def export_dict(self) -> Dict[str, Any]:
        # Return a deep copy to avoid accidental mutation
        import copy

        return copy.deepcopy(self._metrics)