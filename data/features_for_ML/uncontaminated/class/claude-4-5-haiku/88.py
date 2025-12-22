class VacuumPumpMock:

    def __init__(self, port: str = "COM6"):
        self._port = port
        self._status = "CLOSED"
        self._is_open = False

    @property
    def status(self) -> str:
        return self._status

    def get_status(self) -> str:
        return self._status

    def set_status(self, string):
        self._status = string

    def open(self):
        self._is_open = True
        self._status = "OPEN"

    def close(self):
        self._is_open = False
        self._status = "CLOSED"

    def is_open(self):
        return self._is_open

    def is_closed(self):
        return not self._is_open