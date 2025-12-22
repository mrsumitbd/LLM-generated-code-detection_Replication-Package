import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class WatcherHealthServer:
    """Simple HTTP health endpoint for watcher monitoring."""

    def __init__(self, watcher, port=8080):
        self.watcher = watcher
        self.port = port
        self.server = None
        self.thread = None
        self.is_running = False

    def setup_routes(self):
        """Setup HTTP routes for health checks."""
        server = self
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/health':
                    response = {
                        'status': 'healthy',
                        'timestamp': datetime.now().isoformat(),
                        'watcher_active': server.watcher.is_running if hasattr(server.watcher, 'is_running') else True
                    }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                elif self.path == '/status':
                    response = {
                        'status': 'running',
                        'timestamp': datetime.now().isoformat(),
                        'watcher_type': type(server.watcher).__name__
                    }
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Not found'}).encode())
            
            def log_message(self, format, *args):
                pass
        
        self.server = HTTPServer(('localhost', self.port), HealthHandler)
        return self.server

    def start(self):
        """Start the health server in a background thread."""
        if not self.server:
            self.setup_routes()
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

    def _run_server(self):
        """Run the HTTP server."""
        while self.is_running:
            self.server.handle_request()

    def stop(self):
        """Stop the health server."""
        self.is_running = False
        if self.server:
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=1)