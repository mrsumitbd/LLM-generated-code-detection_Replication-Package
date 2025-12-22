import socketserver
import os
import threading
import http.server
from pathlib import Path

def start_http_server(directory, port=None):
    """Start an HTTP server in the given directory.

    Args:
        directory: Directory to serve files from
        port: Port to use (finds a free port if None)

    Returns:
        tuple: (server_thread, port)
    """
    if port is None:
        port = find_free_port()

    # Get the absolute path of the directory
    directory = str(Path(directory).absolute())

    # Change to the directory to serve files
    os.chdir(directory)

    # Create HTTP server
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    # Start server in a separate thread
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = (
        True  # This makes the thread exit when the main program exits
    )
    server_thread.start()

    print(f"Server started at http://localhost:{port}")
    return server_thread, port