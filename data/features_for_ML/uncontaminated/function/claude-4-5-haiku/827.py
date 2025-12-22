import http.server
import socketserver
import threading
import socket

def start_http_server(directory, port=None):
    """Start an HTTP server in the given directory.

    Args:
        directory: Directory to serve files from
        port: Port to use (finds a free port if None)

    Returns:
        tuple: (server_thread, port)
    """
    # If port is None, find a free port
    if port is None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
    
    # Change to the specified directory
    import os
    original_dir = os.getcwd()
    os.chdir(directory)
    
    # Create a custom handler that serves from the current directory
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)
    
    # Create the server
    with socketserver.TCPServer(("", port), Handler) as httpd:
        # Create and start the server thread
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        
        # Store the server instance so it can be shut down later if needed
        server_thread.httpd = httpd
        
        return (server_thread, port)