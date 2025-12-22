import socket
from typing import Any
from api_client import APIClient

class ContainerProc:

    def __init__(self, sock: socket.socket, client: APIClient, exec_id: Any) -> None:
        self.sock = sock
        self.client = client
        self.exec_id = exec_id

    def write_stdin(self, data: bytes) -> None:
        self.sock.sendall(data)

    def close_stdin(self) -> None:
        self.sock.shutdown(socket.SHUT_WR)

    def is_running(self) -> bool:
        return not self.sock._closed

    def read_output(self, timeout_sec: float = 0) -> tuple[int | None, bytes]:
        ready = select.select([self.sock], [], [], timeout_sec)
        if ready[0]:
            data = self.sock.recv(4096)
            return len(data), data
        return None, b''