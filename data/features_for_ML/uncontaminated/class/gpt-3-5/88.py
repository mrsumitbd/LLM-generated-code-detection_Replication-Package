class VacuumPumpMock:

    def __init__(self, port: str = "COM6"):
        self.port = port
        self._status = "closed"

    @property
    def status(self) -> str:
        return self._status

    def get_status(self) -> str:
        return self._status

    def set_status(self, string):
        self._status = string

    def open(self):
        self._status = "open"

    def close(self):
        self._status = "closed"

    def is_open(self):
        return self._status == "open"

    def is_closed(self):
        return self._status == "closed"