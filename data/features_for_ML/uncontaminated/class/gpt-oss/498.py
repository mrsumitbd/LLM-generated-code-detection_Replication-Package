import socket
import threading
import re
from typing import List, Optional


class AgvNavigator:
    """
    A simple AGV (Automated Guided Vehicle) navigator that communicates with a
    remote host over TCP. The host string should be in the form "host:port".
    """

    def __init__(self, host: str):
        """
        Create a connection to the AGV controller.

        :param host: A string in the form "hostname:port".
        """
        self._host, self._port = self._parse_host(host)
        self._lock = threading.Lock()
        self._socket: Optional[socket.socket] = None
        self._connect()

    @staticmethod
    def _parse_host(host: str):
        if ':' not in host:
            raise ValueError("Host must be in the form 'hostname:port'")
        host_part, port_part = host.split(':', 1)
        return host_part, int(port_part)

    def _connect(self):
        """Establish a TCP connection to the AGV controller."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(5.0)
        self._socket.connect((self._host, self._port))

    @property
    def pose(self) -> List[float]:
        """
        Return the current pose of the AGV as a list of floats [x, y, z].
        The pose is extracted from the status string.
        """
        status = self.status
        match = re.search(r'POSE:\s*([-\d\.]+),\s*([-\d\.]+),\s*([-\d\.]+)', status)
        if match:
            return [float(match.group(i)) for i in range(1, 4)]
        return []

    @property
    def status(self) -> str:
        """
        Retrieve the current status string from the AGV.
        """
        try:
            self.send("GET_STATUS")
            response = self._receive()
            return response.strip()
        except Exception:
            return ""

    def send(self, cmd: str, ex_data: str = '', obj: str = 'receive_socket'):
        """
        Send a command to the AGV. The command is sent as a UTF-8 encoded
        string terminated by a newline. Optional ex_data can be appended
        after a space.

        :param cmd: The command string.
        :param ex_data: Optional additional data.
        :param obj: Name of the socket attribute to use (default: 'receive_socket').
        """
        if not hasattr(self, obj):
            raise AttributeError(f"Object '{obj}' not found on instance.")
        sock: socket.socket = getattr(self, obj)
        if sock is None:
            raise ConnectionError("Socket is not connected.")
        message = f"{cmd} {ex_data}".strip() + "\n"
        with self._lock:
            sock.sendall(message.encode('utf-8'))

    def _receive(self, buffer_size: int = 4096) -> str:
        """
        Receive data from the socket until a newline is encountered.
        """
        data = bytearray()
        while True:
            chunk = self._socket.recv(buffer_size)
            if not chunk:
                break
            data.extend(chunk)
            if b'\n' in chunk:
                break
        return data.decode('utf-8')

    def send_nav_task(self, command: str):
        """
        Send a navigation task command to the AGV.

        :param command: The navigation command string.
        """
        self.send("NAV_TASK", command)

    def __del__(self):
        """
        Clean up the socket connection when the object is destroyed.
        """
        try:
            if self._socket:
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
        except Exception:
            pass