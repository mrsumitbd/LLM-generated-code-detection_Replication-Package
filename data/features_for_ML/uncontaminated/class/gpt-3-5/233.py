from typing import Optional

class GrblCNCAsync:

    def __init__(self, port: str, address: str = "1", limits: tuple[int, int, int, int, int, int] = (-150, 150, -200, 0, 0, 60)):
        self.port = port
        self.address = address
        self.limits = limits

    def _read_all(self):
        pass

    def _parse(self, data: bytes, dtype: Optional[type] = None):
        pass

    def _receive(self, data: bytes):
        pass

    @property
    def status(self) -> str:
        pass

    @property
    def position(self) -> Point3D:
        pass

    def get_position(self):
        pass

    @staticmethod
    def list():
        pass