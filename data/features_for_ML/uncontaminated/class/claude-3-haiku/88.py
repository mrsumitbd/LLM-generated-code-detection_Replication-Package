import serial

class VacuumPumpMock:
    def __init__(self, port: str = "COM6"):
        self._port = port
        self._serial = serial.Serial(self._port, 9600, timeout=1)
        self._status = "closed"

    @property
    def status(self) -> str:
        return self._status

    def get_status(self) -> str:
        return self._status

    def set_status(self, string):
        self._status = string

    def open(self):
        self._serial.write(b"open\n")
        self._status = "open"

    def close(self):
        self._serial.write(b"close\n")
        self._status = "closed"

    def is_open(self):
        return self._status == "open"

    def is_closed(self):
        return self._status == "closed"