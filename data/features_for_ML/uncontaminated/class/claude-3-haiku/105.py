import socket
from typing import Any

class ContainerProc:
    def __init__(self, sock: socket.socket, client: APIClient, exec_id: Any) -> None:
        self.sock = sock
        self.client = client
        self.exec_id = exec_id
        self.is_closed = False

    def write_stdin(self, data: bytes) -> None:
        if not self.is_closed:
            self.sock.sendall(data)

    def close_stdin(self) -> None:
        if not self.is_closed:
            self.sock.shutdown(socket.SHUT_WR)
            self.is_closed = True

    def is_running(self) -> bool:
        if self.is_closed:
            return False
        try:
            self.client.inspect_container(self.exec_id)
            return True
        except:
            return False

    def read_output(self, timeout_sec: float = 0) -> tuple[int | None, bytes]:
        if self.is_closed:
            return None, b''
        self.sock.settimeout(timeout_sec)
        try:
            data = self.sock.recv(4096)
            return len(data), data
        except socket.timeout:
            return None, b''
        except:
            self.is_closed = True
            return None, b''