
class DeviceIdentification:
    """PCIe device identification parameters."""

    vendor_id: int
    device_id: int
    class_code: int  # Must be explicitly specified - no default for security
    subsystem_vendor_id: int = 0x0000
    subsystem_device_id: int = 0x0000

    def __post_init__(self):
        """Convert string values to integers if needed."""
        # Convert vendor_id
        if isinstance(self.vendor_id, str):
            self.vendor_id = self._convert_to_int(self.vendor_id)

        # Convert device_id
        if isinstance(self.device_id, str):
            self.device_id = self._convert_to_int(self.device_id)

        # Convert class_code
        if isinstance(self.class_code, str):
            self.class_code = self._convert_to_int(self.class_code)

        # Convert subsystem IDs
        if isinstance(self.subsystem_vendor_id, str):
            self.subsystem_vendor_id = self._convert_to_int(self.subsystem_vendor_id)

        if isinstance(self.subsystem_device_id, str):
            self.subsystem_device_id = self._convert_to_int(self.subsystem_device_id)

    @staticmethod
    def _convert_to_int(value) -> int:
        """Convert hex string or other value to int."""
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            if value.startswith(("0x", "0X")):
                return int(value, 16)
            else:
                return int(value, 0)  # Auto-detect base
        else:
            return int(value)

    def validate(self) -> None:
        """Validate device identification values."""
        if not (0x0001 <= self.vendor_id <= 0xFFFE):
            raise ValueError(f"Invalid vendor ID: 0x{self.vendor_id:04X}")
        if not (0x0001 <= self.device_id <= 0xFFFF):
            raise ValueError(f"Invalid device ID: 0x{self.device_id:04X}")
        if not (0x000000 <= self.class_code <= 0xFFFFFF):
            raise ValueError(f"Invalid class code: 0x{self.class_code:06X}")

    @property
    def vendor_id_hex(self) -> str:
        """Get vendor ID as hex string."""
        return f"0x{self.vendor_id:04X}"

    @property
    def device_id_hex(self) -> str:
        """Get device ID as hex string."""
        return f"0x{self.device_id:04X}"

    @property
    def class_code_hex(self) -> str:
        """Get class code as hex string."""
        return f"0x{self.class_code:06X}"