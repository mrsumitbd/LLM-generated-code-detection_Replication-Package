class DeviceIdentification:
    """PCIe device identification parameters."""

    def __init__(self, vendor_id: int, device_id: int, class_code: int):
        self._vendor_id = vendor_id
        self._device_id = device_id
        self._class_code = class_code

    def __post_init__(self):
        self.validate()

    @staticmethod
    def _convert_to_int(value) -> int:
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            return int(value, 16)
        else:
            raise ValueError("Value must be an integer or a hexadecimal string.")

    def validate(self) -> None:
        self._vendor_id = self._convert_to_int(self._vendor_id)
        self._device_id = self._convert_to_int(self._device_id)
        self._class_code = self._convert_to_int(self._class_code)

    @property
    def vendor_id_hex(self) -> str:
        return f"{self._vendor_id:04X}"

    @property
    def device_id_hex(self) -> str:
        return f"{self._device_id:04X}"

    @property
    def class_code_hex(self) -> str:
        return f"{self._class_code:06X}"