class TCL_SplitAC_Fresh_Air_DeviceData:

    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state
        self.delta = delta

# Example usage:
# device_data = TCL_SplitAC_Fresh_Air_DeviceData("12345", {"temperature": 25, "humidity": 50}, {"temperature": 26})