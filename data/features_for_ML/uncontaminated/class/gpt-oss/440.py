import asyncio
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float


class MockCNCAsync:
    def __init__(self):
        self._position: Point3D = Point3D(0.0, 0.0, 0.0)
        self._status: str = "idle"

    @property
    def position(self) -> Point3D:
        return self._position

    @property
    def status(self) -> str:
        return self._status

    async def move_to(self, target: Point3D, speed: float = 100.0) -> None:
        """
        Simulate moving the CNC head to the target position asynchronously.
        The time taken is proportional to the Euclidean distance divided by speed.
        """
        if self._status == "moving":
            raise RuntimeError("CNC is already moving")

        self._status = "moving"
        dx = target.x - self._position.x
        dy = target.y - self._position.y
        dz = target.z - self._position.z
        distance = (dx**2 + dy**2 + dz**2) ** 0.5
        # Avoid division by zero
        delay = distance / speed if speed > 0 else 0
        await asyncio.sleep(delay)
        self._position = target
        self._status = "idle"