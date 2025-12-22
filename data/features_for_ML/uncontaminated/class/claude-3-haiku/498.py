import socket
import json

class AgvNavigator:

    def __init__(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, 8080))

    @property
    def pose(self) -> list:
        self.send('get_pose')
        response = self.receive_socket()
        return json.loads(response)

    @property
    def status(self) -> str:
        self.send('get_status')
        response = self.receive_socket()
        return response

    def send(self, cmd, ex_data='', obj='receive_socket'):
        data = {'cmd': cmd, 'ex_data': ex_data}
        self.socket.sendall(json.dumps(data).encode())
        if obj == 'receive_socket':
            return self.receive_socket()

    def send_nav_task(self, command: str):
        self.send('nav_task', command)

    def receive_socket(self):
        data = b''
        while True:
            packet = self.socket.recv(4096)
            if not packet:
                break
            data += packet
        return data.decode()

    def __del__(self):
        self.socket.close()