import http.server
import socketserver
import threading
import socket

def start_http_server(directory, port=None):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

    class ThreadedHTTPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    if port is None:
        port = 0

    server = ThreadedHTTPServer(('localhost', port), Handler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    port = server.server_address[1]
    return server_thread, port