class TCL_SplitAC_DeviceData:
    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state
        self.delta = delta

        self.power_state = self.aws_thing_state.get("power_state", False)
        self.temperature = self.aws_thing_state.get("temperature", 0)
        self.mode = self.aws_thing_state.get("mode", "")
        self.fan_speed = self.aws_thing_state.get("fan_speed", "")
        self.swing = self.aws_thing_state.get("swing", "")

        self.power_state_delta = self.delta.get("power_state", None)
        self.temperature_delta = self.delta.get("temperature", None)
        self.mode_delta = self.delta.get("mode", None)
        self.fan_speed_delta = self.delta.get("fan_speed", None)
        self.swing_delta = self.delta.get("swing", None)