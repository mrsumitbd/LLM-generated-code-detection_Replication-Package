from dataclasses import dataclass

@dataclass
class Point3D:
    x: float
    y: float
    z: float

class MockCNCAsync:
    def __init__(self):
        self._position = Point3D(0.0, 0.0, 0.0)
        self._status = "Idle"

    @property
    def position(self) -> Point3D:
        return self._position

    @property
    def status(self) -> str:
        return self._status

    def move_to(self, x: float, y: float, z: float):
        self._position = Point3D(x, y, z)
        self._status = "Moving"

    async def move_async(self, x: float, y: float, z: float):
        self.move_to(x, y, z)
        self._status = "Idle"

    async def wait_until_idle(self):
        while self._status == "Moving":
            pass