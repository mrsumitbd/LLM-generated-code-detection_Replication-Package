from dataclasses import dataclass, field
from typing import Union


@dataclass
class DeviceIdentification:
    """PCIe device identification parameters."""

    vendor_id: Union[int, str] = field(default=0)
    device_id: Union[int, str] = field(default=0)
    class_code: Union[int, str] = field(default=0)

    def __post_init__(self) -> None:
        # Convert all fields to integers
        self.vendor_id = self._convert_to_int(self.vendor_id)
        self.device_id = self._convert_to_int(self.device_id)
        self.class_code = self._convert_to_int(self.class_code)
        # Validate the converted values
        self.validate()

    @staticmethod
    def _convert_to_int(value: Union[int, str]) -> int:
        """Convert a value to an integer. Accepts int, hex string with or without '0x'."""
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            value = value.strip()
            if value.lower().startswith("0x"):
                return int(value, 16)
            # Assume decimal if no prefix
            return int(value, 10)
        raise TypeError(f"Unsupported type for conversion: {type(value).__name__}")

    def validate(self) -> None:
        """Validate that the identification parameters are within PCIe ranges."""
        if not (0 <= self.vendor_id <= 0xFFFF):
            raise ValueError(f"vendor_id {self.vendor_id:#06x} out of range (0x0000–0xFFFF)")
        if not (0 <= self.device_id <= 0xFFFF):
            raise ValueError(f"device_id {self.device_id:#06x} out of range (0x0000–0xFFFF)")
        if not (0 <= self.class_code <= 0xFFFFFF):
            raise ValueError(f"class_code {self.class_code:#08x} out of range (0x000000–0xFFFFFF)")

    @property
    def vendor_id_hex(self) -> str:
        """Vendor ID as a 4‑digit hexadecimal string."""
        return f"{self.vendor_id:04X}"

    @property
    def device_id_hex(self) -> str:
        """Device ID as a 4‑digit hexadecimal string."""
        return f"{self.device_id:04X}"

    @property
    def class_code_hex(self) -> str:
        """Class code as a 6‑digit hexadecimal string."""
        return f"{self.class_code:06X}"