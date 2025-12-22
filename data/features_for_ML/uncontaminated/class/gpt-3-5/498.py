class AgvNavigator:

    def __init__(self, host):
        self.host = host
        self.pose = [0, 0, 0]
        self.status = "Idle"

    @property
    def pose(self) -> list:
        return self._pose

    @property
    def status(self) -> str:
        return self._status

    def send(self, cmd, ex_data='', obj='receive_socket'):
        print(f"Sending command '{cmd}' with extra data '{ex_data}' to object '{obj}'")

    def send_nav_task(self, command: str):
        print(f"Sending navigation task: {command}")

    def __del__(self):
        print("AGV Navigator instance deleted")