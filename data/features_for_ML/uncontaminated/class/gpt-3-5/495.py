import subprocess
import os

class ManagedAPIServer:
    """Context manager for subprocess-managed OpenHands API server."""

    def __init__(self, port: int = 8000, host: str = "127.0.0.1"):
        self.port = port
        self.host = host
        self.process = None

    def __enter__(self):
        command = f"python -m http.server {self.port}"
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.process.terminate()
        self.process.wait()

if __name__ == "__main__":
    with ManagedAPIServer() as server:
        print(f"API server running on {server.host}:{server.port}")
        input("Press Enter to stop the server...")