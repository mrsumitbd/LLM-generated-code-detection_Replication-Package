class MetricsCollector:
    """Enhanced metrics collector with full dashboard support"""
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, enable: bool = True):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, enable: bool = True):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.enable = enable
        self.metrics = {
            'session_count': 0,
            'active_sessions': 0,
            'blocked_commands': 0,
            'llm_queries': 0,
            'llm_query_duration': 0.0,
            'rate_limits': 0,
            'health': True,
            'blocked_by_reason': {},
            'llm_query_status': {},
            'session_start_time': None,
            'last_updated': None,
        }
        self.sessions = {}
        self.server_thread = None
        self.server = None
        self._lock = threading.Lock()

    def session_start(self):
        if not self.enable:
            return
        with self._lock:
            session_id = str(uuid.uuid4())
            self.metrics['session_count'] += 1
            self.metrics['active_sessions'] += 1
            self.sessions[session_id] = {
                'start_time': time.time(),
                'commands': 0,
                'queries': 0,
            }
            self.metrics['session_start_time'] = time.time()
            self.metrics['last_updated'] = time.time()
            return session_id

    def session_end(self):
        if not self.enable:
            return
        with self._lock:
            if self.metrics['active_sessions'] > 0:
                self.metrics['active_sessions'] -= 1
            self.metrics['last_updated'] = time.time()

    def record_blocked_command(self, reason: str = "blacklist"):
        if not self.enable:
            return
        with self._lock:
            self.metrics['blocked_commands'] += 1
            if reason not in self.metrics['blocked_by_reason']:
                self.metrics['blocked_by_reason'][reason] = 0
            self.metrics['blocked_by_reason'][reason] += 1
            self.metrics['last_updated'] = time.time()

    def record_llm_query(self, duration: float, status: str = "success"):
        if not self.enable:
            return
        with self._lock:
            self.metrics['llm_queries'] += 1
            self.metrics['llm_query_duration'] += duration
            if status not in self.metrics['llm_query_status']:
                self.metrics['llm_query_status'][status] = 0
            self.metrics['llm_query_status'][status] += 1
            self.metrics['last_updated'] = time.time()

    def record_rate_limit(self, session_id: str):
        if not self.enable:
            return
        with self._lock:
            self.metrics['rate_limits'] += 1
            self.metrics['last_updated'] = time.time()

    def set_health(self, healthy: bool):
        if not self.enable:
            return
        with self._lock:
            self.metrics['health'] = healthy
            self.metrics['last_updated'] = time.time()

    def start_server(self, port: int = 8000) -> bool:
        if not self.enable:
            return False
        try:
            from flask import Flask, jsonify
            app = Flask(__name__)
            
            @app.route('/metrics', methods=['GET'])
            def get_metrics():
                with self._lock:
                    return jsonify(self.metrics)
            
            @app.route('/health', methods=['GET'])
            def health():
                with self._lock:
                    return jsonify({'healthy': self.metrics['health']})
            
            def run_server():
                app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
            
            self.server_thread = threading.Thread(target=run_server, daemon=True)
            self.server_thread.start()
            return True
        except Exception as e:
            return False

    def track_performance(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                self.record_llm_query(duration, status="success")
                return result
            except Exception as e:
                duration = time.time() - start_time
                self.record_llm_query(duration, status="error")
                raise
        return wrapper

    def export(self) -> str:
        if not self.enable:
            return "{}"
        with self._lock:
            return json.dumps(self.metrics, indent=2, default=str)