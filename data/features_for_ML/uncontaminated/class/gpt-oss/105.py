import socket
import select
from typing import Any, Tuple, Optional

class ContainerProc:
    """
    A helper class to interact with a Docker container exec instance via a socket.
    """

    def __init__(self, sock: socket.socket, client: Any, exec_id: Any) -> None:
        """
        Initialize the ContainerProc.

        :param sock: The socket connected to the exec stream.
        :param client: The Docker API client (must provide exec_inspect).
        :param exec_id: The exec instance ID.
        """
        self._sock = sock
        self._client = client
        self._exec_id = exec_id
        # Ensure the socket is non‑blocking for select usage
        self._sock.setblocking(False)

    def write_stdin(self, data: bytes) -> None:
        """
        Write data to the exec's stdin.

        :param data: Bytes to send.
        """
        if not data:
            return
        try:
            self._sock.sendall(data)
        except BrokenPipeError:
            # The exec process has closed stdin; ignore
            pass

    def close_stdin(self) -> None:
        """
        Close the write side of the socket to signal EOF to the exec process.
        """
        try:
            self._sock.shutdown(socket.SHUT_WR)
        except OSError:
            # Socket already closed or not connected
            pass

    def is_running(self) -> bool:
        """
        Check whether the exec process is still running.

        :return: True if running, False otherwise.
        """
        try:
            info = self._client.exec_inspect(self._exec_id)
            return bool(info.get("Running", False))
        except Exception:
            # If we cannot inspect, assume it's not running
            return False

    def read_output(self, timeout_sec: float = 0) -> Tuple[Optional[int], bytes]:
        """
        Read available output from the exec stream.

        :param timeout_sec: Timeout in seconds for the read operation.
                            0 means non‑blocking.
        :return: A tuple of (exit_code or None, bytes read).
        """
        data = bytearray()
        exit_code: Optional[int] = None

        # Loop until no more data or timeout
        while True:
            rlist, _, _ = select.select([self._sock], [], [], timeout_sec)
            if not rlist:
                # Timeout or no data ready
                break

            try:
                chunk = self._sock.recv(4096)
            except BlockingIOError:
                # No data available right now
                break

            if not chunk:
                # Socket closed – exec finished
                try:
                    info = self._client.exec_inspect(self._exec_id)
                    exit_code = info.get("ExitCode")
                except Exception:
                    exit_code = None
                break

            data.extend(chunk)

        return exit_code, bytes(data)