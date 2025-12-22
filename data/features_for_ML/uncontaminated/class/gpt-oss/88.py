class VacuumPumpMock:
    def __init__(self, port: str = "COM6"):
        self.port = port
        self._open = False
        self._status = "closed"

    @property
    def status(self) -> str:
        return self._status

    def get_status(self) -> str:
        return self._status

    def set_status(self, string: str):
        self._status = string

    def open(self):
        self._open = True
        self._status = "open"

    def close(self):
        self._open = False
        self._status = "closed"

    def is_open(self):
        return self._open

    def is_closed(self):
        return not self._open