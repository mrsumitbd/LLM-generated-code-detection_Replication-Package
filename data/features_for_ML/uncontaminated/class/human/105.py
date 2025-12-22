import select
from docker import APIClient
import socket
from typing import Any

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
        exec_inspect = self.client.exec_inspect(self.exec_id)
        return exec_inspect["Running"]

    def read_output(self, timeout_sec: float = 0) -> tuple[int | None, bytes]:
        """First value in tuple is one of:
        0: no data to read within specified timeout
        1: stdout
        2: stderr
        None: process has ended

        Second value in tuple is the data read from the stream.
        """
        rlist, _, _ = select.select([self.sock], [], [], timeout_sec)
        if self.sock in rlist:
            return _demux_multiplexed_stream(self.sock)
        else:
            return 0, b""