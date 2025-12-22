import serial
import serial.tools.list_ports
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class Point3D:
    x: float
    y: float
    z: float


class GrblCNCAsync:
    """
    Simple asynchronous GRBL interface.
    """

    def __init__(
        self,
        port: str,
        address: str = "1",
        limits: Tuple[int, int, int, int, int, int] = (-150, 150, -200, 0, 0, 60),
    ):
        """
        Open the serial port and initialise internal state.
        """
        self.port = port
        self.address = address
        self.limits = limits

        # Serial configuration – GRBL defaults to 115200 baud
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            timeout=0.1,
            write_timeout=0.1,
        )
        # Flush any stale data
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        # Internal state
        self._status: str = ""
        self._position: Point3D = Point3D(0.0, 0.0, 0.0)

    # ------------------------------------------------------------------
    # Low‑level helpers
    # ------------------------------------------------------------------
    def _read_all(self) -> bytes:
        """
        Read all available data from the serial port.
        """
        data = bytearray()
        while self.ser.in_waiting:
            data += self.ser.read(self.ser.in_waiting)
        return bytes(data)

    def _parse(self, data: bytes, dtype: Optional[type] = None):
        """
        Convert raw bytes to a string or a numeric type.
        """
        text = data.decode("utf-8", errors="ignore").strip()
        if dtype is None:
            return text
        try:
            return dtype(text)
        except ValueError:
            return None

    def _receive(self, data: bytes):
        """
        Process incoming data, updating status and position.
        """
        # Split on newlines – GRBL uses CRLF
        for line in data.splitlines():
            line = line.decode("utf-8", errors="ignore").strip()
            if not line:
                continue

            # Status line: <Idle (MPos:0.000,0.000,0.000)>
            if line.startswith("<") and line.endswith(">"):
                self._status = line
                # Extract machine position
                try:
                    pos_part = line.split("MPos:")[1]
                    pos_str = pos_part.split(")")[0]
                    x_str, y_str, z_str = pos_str.split(",")
                    self._position = Point3D(
                        float(x_str), float(y_str), float(z_str)
                    )
                except Exception:
                    # Malformed status – ignore
                    pass
            # OK or error messages – ignore for now
            elif line.startswith("ok") or line.startswith("error"):
                pass
            else:
                # Other messages – store as status
                self._status = line

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def status(self) -> str:
        """
        Return the most recent status string.
        """
        # Update status by reading any pending data
        raw = self._read_all()
        if raw:
            self._receive(raw)
        return self._status

    @property
    def position(self) -> Point3D:
        """
        Return the most recent machine position.
        """
        # Update position by reading any pending data
        raw = self._read_all()
        if raw:
            self._receive(raw)
        return self._position

    def get_position(self) -> Point3D:
        """
        Convenience wrapper – returns the current position.
        """
        return self.position

    @staticmethod
    def list() -> List[str]:
        """
        Return a list of available serial ports.
        """
        return [port.device for port in serial.tools.list_ports.comports()]