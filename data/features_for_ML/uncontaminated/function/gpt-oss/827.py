import os
import socket
import threading
import http.server
import socketserver
from functools import partial

def start_http_server(directory, port=None):
    """Start an HTTP server in the given directory.

    Args:
        directory: Directory to serve files from
        port: Port to use (finds a free port if None)

    Returns:
        tuple: (server_thread, port)
    """
    # Ensure directory exists
    if not os.path.isdir(directory):
        raise ValueError(f"Directory does not exist: {directory}")

    # Create a handler that serves from the specified directory
    handler_cls = partial(http.server.SimpleHTTPRequestHandler, directory=directory)

    # Bind to the requested port or find a free one
    bind_address = ('0.0.0.0', port if port is not None else 0)

    # Use ThreadingTCPServer to allow concurrent requests
    server = socketserver.ThreadingTCPServer(bind_address, handler_cls)

    # Retrieve the actual port (useful if port was 0)
    actual_port = server.server_address[1]

    # Run the server in a separate thread
    def serve():
        try:
            server.serve_forever()
        finally:
            server.server_close()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()

    return thread, actual_port