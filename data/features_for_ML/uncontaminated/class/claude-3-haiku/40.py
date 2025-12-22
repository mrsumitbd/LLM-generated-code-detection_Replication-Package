class TCL_SplitAC_Fresh_Air_DeviceData:
    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state
        self.delta = delta

        self.power_state = self.aws_thing_state.get("power_state", False)
        self.fan_speed = self.aws_thing_state.get("fan_speed", 0)
        self.temperature = self.aws_thing_state.get("temperature", 0)
        self.fresh_air_mode = self.aws_thing_state.get("fresh_air_mode", False)
        self.fresh_air_percentage = self.aws_thing_state.get("fresh_air_percentage", 0)

        self.power_state_delta = self.delta.get("power_state", None)
        self.fan_speed_delta = self.delta.get("fan_speed", None)
        self.temperature_delta = self.delta.get("temperature", None)
        self.fresh_air_mode_delta = self.delta.get("fresh_air_mode", None)
        self.fresh_air_percentage_delta = self.delta.get("fresh_air_percentage", None)