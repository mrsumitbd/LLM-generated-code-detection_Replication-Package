import subprocess
import sys
import time
import socket
import os
import signal
from contextlib import contextmanager

class ManagedAPIServer:
    """Context manager for subprocess-managed OpenHands API server."""

    def __init__(self, port: int = 8000, host: str = "127.0.0.1"):
        self.port = port
        self.host = host
        self.process: subprocess.Popen | None = None

    def __enter__(self):
        # Start the OpenHands API server as a subprocess
        cmd = [
            sys.executable,
            "-m",
            "openhands.server",
            "--host",
            self.host,
            "--port",
            str(self.port),
        ]
        # Redirect stdout/stderr to pipes so we can read them if needed
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        # Wait until the server is listening on the specified port
        timeout = 30  # seconds
        start = time.time()
        while True:
            if self.process.poll() is not None:
                # Process exited prematurely
                stdout, stderr = self.process.communicate()
                raise RuntimeError(
                    f"OpenHands server exited unexpectedly.\n"
                    f"stdout:\n{stdout}\n"
                    f"stderr:\n{stderr}"
                )
            try:
                with socket.create_connection((self.host, self.port), timeout=1):
                    break  # Successfully connected
            except (ConnectionRefusedError, socket.timeout):
                if time.time() - start > timeout:
                    # Timeout reached
                    self.process.terminate()
                    stdout, stderr = self.process.communicate()
                    raise RuntimeError(
                        f"OpenHands server did not start within {timeout}s.\n"
                        f"stdout:\n{stdout}\n"
                        f"stderr:\n{stderr}"
                    )
                time.sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.process is None:
            return
        # Attempt graceful shutdown
        try:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        finally:
            self.process = None