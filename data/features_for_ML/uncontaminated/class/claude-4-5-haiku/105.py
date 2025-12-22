import socket
import select
from typing import Any

class ContainerProc:

    def __init__(self, sock: socket.socket, client: APIClient, exec_id: Any) -> None:
        self.sock = sock
        self.client = client
        self.exec_id = exec_id
        self._stdin_closed = False

    def write_stdin(self, data: bytes) -> None:
        if self._stdin_closed:
            raise ValueError("stdin is already closed")
        try:
            self.sock.sendall(data)
        except (socket.error, BrokenPipeError) as e:
            raise IOError(f"Failed to write to stdin: {e}")

    def close_stdin(self) -> None:
        if not self._stdin_closed:
            try:
                self.sock.shutdown(socket.SHUT_WR)
            except (socket.error, OSError):
                pass
            self._stdin_closed = True

    def is_running(self) -> bool:
        try:
            result = self.client.exec_inspect(self.exec_id)
            return result.get('Running', False)
        except Exception:
            return False

    def read_output(self, timeout_sec: float = 0) -> tuple[int | None, bytes]:
        output = b''
        exit_code = None
        
        try:
            self.sock.settimeout(timeout_sec if timeout_sec > 0 else None)
            
            while True:
                try:
                    data = self.sock.recv(4096)
                    if not data:
                        break
                    output += data
                except socket.timeout:
                    break
                except (socket.error, OSError):
                    break
            
            if not self.is_running():
                result = self.client.exec_inspect(self.exec_id)
                exit_code = result.get('ExitCode')
        
        except Exception:
            pass
        finally:
            try:
                self.sock.settimeout(None)
            except (socket.error, OSError):
                pass
        
        return exit_code, output