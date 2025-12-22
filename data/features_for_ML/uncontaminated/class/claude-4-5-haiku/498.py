import socket
import json
import time
from threading import Thread, Lock

class AgvNavigator:

    def __init__(self, host):
        self.host = host
        self.port = 8080
        self.socket = None
        self._pose = [0.0, 0.0, 0.0]
        self._status = "idle"
        self._lock = Lock()
        self._running = True
        self._connect()
        self._receiver_thread = Thread(target=self._receive_loop, daemon=True)
        self._receiver_thread.start()

    def _connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
        except Exception as e:
            print(f"Connection error: {e}")
            self.socket = None

    def _receive_loop(self):
        while self._running:
            try:
                if self.socket:
                    data = self.socket.recv(1024)
                    if data:
                        self._parse_response(data)
                    else:
                        self._reconnect()
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Receive error: {e}")
                self._reconnect()
            time.sleep(0.1)

    def _reconnect(self):
        try:
            if self.socket:
                self.socket.close()
        except:
            pass
        time.sleep(1)
        self._connect()

    def _parse_response(self, data):
        try:
            message = data.decode('utf-8')
            response = json.loads(message)
            
            with self._lock:
                if 'pose' in response:
                    self._pose = response['pose']
                if 'status' in response:
                    self._status = response['status']
        except Exception as e:
            print(f"Parse error: {e}")

    @property
    def pose(self) -> list:
        with self._lock:
            return self._pose.copy()

    @property
    def status(self) -> str:
        with self._lock:
            return self._status

    def send(self, cmd, ex_data='', obj='receive_socket'):
        try:
            if not self.socket:
                self._connect()
            
            message = {
                'cmd': cmd,
                'ex_data': ex_data,
                'obj': obj
            }
            
            json_message = json.dumps(message)
            self.socket.sendall(json_message.encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")
            self._reconnect()

    def send_nav_task(self, command: str):
        try:
            if not self.socket:
                self._connect()
            
            message = {
                'type': 'nav_task',
                'command': command
            }
            
            json_message = json.dumps(message)
            self.socket.sendall(json_message.encode('utf-8'))
        except Exception as e:
            print(f"Navigation task error: {e}")
            self._reconnect()

    def __del__(self):
        self._running = False
        try:
            if self.socket:
                self.socket.close()
        except:
            pass