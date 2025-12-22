class TCL_SplitAC_DeviceData:

    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state
        self.delta = delta