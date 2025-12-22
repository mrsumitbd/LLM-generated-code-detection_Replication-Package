from dataclasses import dataclass
from typing import Union

@dataclass
class DeviceIdentification:
    """PCIe device identification parameters."""
    
    vendor_id: Union[int, str]
    device_id: Union[int, str]
    class_code: Union[int, str]

    def __post_init__(self):
        self.vendor_id = self._convert_to_int(self.vendor_id)
        self.device_id = self._convert_to_int(self.device_id)
        self.class_code = self._convert_to_int(self.class_code)
        self.validate()

    @staticmethod
    def _convert_to_int(value) -> int:
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            if value.startswith(('0x', '0X')):
                return int(value, 16)
            return int(value)
        raise TypeError(f"Cannot convert {type(value)} to int")

    def validate(self) -> None:
        if not (0 <= self.vendor_id <= 0xFFFF):
            raise ValueError(f"vendor_id must be between 0 and 0xFFFF, got {self.vendor_id}")
        if not (0 <= self.device_id <= 0xFFFF):
            raise ValueError(f"device_id must be between 0 and 0xFFFF, got {self.device_id}")
        if not (0 <= self.class_code <= 0xFFFFFF):
            raise ValueError(f"class_code must be between 0 and 0xFFFFFF, got {self.class_code}")

    @property
    def vendor_id_hex(self) -> str:
        return f"0x{self.vendor_id:04X}"

    @property
    def device_id_hex(self) -> str:
        return f"0x{self.device_id:04X}"

    @property
    def class_code_hex(self) -> str:
        return f"0x{self.class_code:06X}"