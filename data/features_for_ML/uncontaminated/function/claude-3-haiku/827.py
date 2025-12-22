import http.server
import socketserver
import threading

def start_http_server(directory, port=None):
    """Start an HTTP server in the given directory.

    Args:
        directory: Directory to serve files from
        port: Port to use (finds a free port if None)

    Returns:
        tuple: (server_thread, port)
    """
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port or 0), Handler) as httpd:
        port = httpd.server_address[1]
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        return server_thread, port