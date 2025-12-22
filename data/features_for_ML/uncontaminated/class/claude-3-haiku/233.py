import asyncio
import serial_asyncio
import re
from typing import Optional, Tuple

class Point3D:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

class GrblCNCAsync:
    def __init__(self, port: str, address: str = "1", limits: Tuple[int, int, int, int, int, int] = (-150, 150, -200, 0, 0, 60)):
        self._port = port
        self._address = address
        self._limits = limits
        self._reader, self._writer = None, None
        self._status = ""
        self._position = Point3D(0, 0, 0)

    async def _read_all(self):
        data = b""
        while True:
            try:
                chunk = await self._reader.read(1024)
                if not chunk:
                    break
                data += chunk
            except asyncio.TimeoutError:
                break
        return data

    def _parse(self, data: bytes, dtype: Optional[type] = None):
        if dtype == str:
            return data.decode().strip()
        elif dtype == Point3D:
            match = re.match(r"X:(-?\d+\.\d+) Y:(-?\d+\.\d+) Z:(-?\d+\.\d+)", data.decode().strip())
            if match:
                return Point3D(float(match.group(1)), float(match.group(2)), float(match.group(3)))
        return data

    def _receive(self, data: bytes):
        if b"ok" in data:
            self._status = "ok"
        elif b"error" in data:
            self._status = "error"
        elif b"Grbl" in data:
            self._status = "ready"
        elif b"MPos:" in data:
            self._position = self._parse(data, dtype=Point3D)

    @property
    def status(self) -> str:
        return self._status

    @property
    def position(self) -> Point3D:
        return self._position

    async def get_position(self):
        self._writer.write(b"?")
        await self._writer.drain()
        data = await self._read_all()
        self._receive(data)
        return self._position

    @staticmethod
    async def list():
        ports = await serial_asyncio.serial_asyncio.list_ports()
        return [port.device for port in ports]

    async def connect(self):
        self._reader, self._writer = await serial_asyncio.open_serial_connection(url=self._port, baudrate=115200)

    async def disconnect(self):
        self._writer.close()
        await self._writer.wait_closed()