from typing import NamedTuple

class Point3D(NamedTuple):
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