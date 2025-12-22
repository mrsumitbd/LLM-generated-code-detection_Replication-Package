class DeviceIdentification:
    """PCIe device identification parameters."""

    def __init__(self, vendor_id: str, device_id: str, class_code: str):
        self.vendor_id = vendor_id
        self.device_id = device_id
        self.class_code = class_code

    @staticmethod
    def _convert_to_int(value) -> int:
        return int(value, 16)

    def validate(self) -> None:
        if len(self.vendor_id) != 4 or len(self.device_id) != 4 or len(self.class_code) != 6:
            raise ValueError("Invalid identification parameters")

    @property
    def vendor_id_hex(self) -> str:
        return self.vendor_id

    @property
    def device_id_hex(self) -> str:
        return self.device_id

    @property
    def class_code_hex(self) -> str:
        return self.class_code