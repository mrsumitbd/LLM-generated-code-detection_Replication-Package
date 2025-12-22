class MockCNCAsync:

    def __init__(self):
        self._position = Point3D(0, 0, 0)
        self._status = "idle"

    @property
    def position(self) -> Point3D:
        return self._position

    @property
    def status(self) -> str:
        return self._status