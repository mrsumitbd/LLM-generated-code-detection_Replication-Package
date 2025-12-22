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

    def __enter__(self):
        # Build the command to start the OpenHands API server.
        # Adjust the command if your installation uses a different entry point.
        cmd = [
            "openhands",
            "api",
            "--host",
            self.host,
            "--port",
            str(self.port),
        ]

        # Start the server subprocess
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait until the server is ready to accept requests
        url = f"http://{self.host}:{self.port}/"
        timeout = 30  # seconds
        start = time.time()
        while True:
            if self.process.poll() is not None:
                # Process exited prematurely
                stdout, stderr = self.process.communicate()
                raise RuntimeError(
                    f"OpenHands API server exited unexpectedly.\n"
                    f"stdout: {stdout}\nstderr: {stderr}"
                )
            try:
                resp = requests.get(url, timeout=1)
                if resp.status_code == 200:
                    break
            except Exception:
                pass
            if time.time() - start > timeout:
                self.process.terminate()
                stdout, stderr = self.process.communicate()
                raise RuntimeError(
                    f"OpenHands API server did not start within {timeout}s.\n"
                    f"stdout: {stdout}\nstderr: {stderr}"
                )
            time.sleep(0.5)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process:
            try:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            finally:
                self.process = None