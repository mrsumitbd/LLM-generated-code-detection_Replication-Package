import socket
import threading

class ScratchGlobalToggle:
    def __init__(self) -> None:
        self.server_socket = None
        self.client_socket = None
        self.is_connected = False
        self.toggle_state = False

    def create_sockets(self) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 8000))
        self.server_socket.listen(1)
        self.client_socket, _ = self.server_socket.accept()
        self.is_connected = True

    def create_nodes(self) -> None:
        def toggle_thread():
            while self.is_connected:
                data = self.client_socket.recv(1024)
                if data:
                    self.toggle_state = not self.toggle_state
                    self.client_socket.sendall(str(self.toggle_state).encode())

        toggle_thread_instance = threading.Thread(target=toggle_thread)
        toggle_thread_instance.start()