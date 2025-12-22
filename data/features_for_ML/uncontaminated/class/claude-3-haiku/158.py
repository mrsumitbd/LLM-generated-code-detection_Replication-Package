import http.server
import socketserver

class WatcherHealthServer:
    """Simple HTTP health endpoint for watcher monitoring."""

    def __init__(self, watcher, port=8080):
        self.watcher = watcher
        self.port = port
        self.httpd = None

    def setup_routes(self):
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/health":
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"OK")
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Not found")

        self.httpd = socketserver.TCPServer(("", self.port), RequestHandler)

    def start(self):
        self.httpd.serve_forever()

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()