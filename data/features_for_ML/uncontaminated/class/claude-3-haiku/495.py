import subprocess
import time
import signal
import os

class ManagedAPIServer:
    """Context manager for subprocess-managed OpenHands API server."""

    def __init__(self, port: int = 8000, host: str = "127.0.0.1"):
        self.port = port
        self.host = host
        self.process = None

    def __enter__(self):
        self.start_server()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_server()

    def start_server(self):
        self.process = subprocess.Popen(
            ["python", "api_server.py", f"--port={self.port}", f"--host={self.host}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # Wait for the server to start
        for _ in range(10):
            if self.process.poll() is None:
                if "Server started" in self.process.stdout.readline():
                    return
            time.sleep(0.5)

        raise RuntimeError("Failed to start the API server")

    def stop_server(self):
        if self.process and self.process.poll() is None:
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
            self.process = None