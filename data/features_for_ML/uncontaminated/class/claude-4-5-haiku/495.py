import subprocess
import time
import requests
from typing import Optional

class ManagedAPIServer:
    """Context manager for subprocess-managed OpenHands API server."""

    def __init__(self, port: int = 8000, host: str = "127.0.0.1"):
        self.port = port
        self.host = host
        self.process: Optional[subprocess.Popen] = None
        self.base_url = f"http://{host}:{port}"

    def __enter__(self):
        # Start the API server
        self.process = subprocess.Popen(
            ["python", "-m", "openhands.server.run"],
            env={"OPENHANDS_PORT": str(self.port), "OPENHANDS_HOST": self.host},
        )
        
        # Wait for server to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=1)
                if response.status_code == 200:
                    return self
            except requests.exceptions.RequestException:
                pass
            time.sleep(0.5)
        
        raise RuntimeError(f"Failed to start API server on {self.base_url}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()