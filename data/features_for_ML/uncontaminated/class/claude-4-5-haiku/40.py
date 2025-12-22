class TCL_SplitAC_Fresh_Air_DeviceData:

    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state
        self.delta = delta
        self.reported = aws_thing_state.get('reported', {})
        self.desired = aws_thing_state.get('desired', {})
        self._parse_device_data()

    def _parse_device_data(self) -> None:
        """Parse and extract device data from aws_thing_state"""
        self.power = self.reported.get('power', 'off')
        self.mode = self.reported.get('mode', 'cool')
        self.temperature = self.reported.get('temperature', 24)
        self.fan_speed = self.reported.get('fan_speed', 'auto')
        self.swing = self.reported.get('swing', 'off')
        self.fresh_air = self.reported.get('fresh_air', 'off')
        self.eco_mode = self.reported.get('eco_mode', 'off')
        self.sleep_mode = self.reported.get('sleep_mode', 'off')

    def get_device_id(self) -> str:
        """Get device ID"""
        return self.device_id

    def get_power_state(self) -> str:
        """Get power state"""
        return self.power

    def get_mode(self) -> str:
        """Get current mode"""
        return self.mode

    def get_temperature(self) -> int:
        """Get set temperature"""
        return self.temperature

    def get_fan_speed(self) -> str:
        """Get fan speed"""
        return self.fan_speed

    def get_swing_state(self) -> str:
        """Get swing state"""
        return self.swing

    def get_fresh_air_state(self) -> str:
        """Get fresh air state"""
        return self.fresh_air

    def get_eco_mode_state(self) -> str:
        """Get eco mode state"""
        return self.eco_mode

    def get_sleep_mode_state(self) -> str:
        """Get sleep mode state"""
        return self.sleep_mode

    def get_delta_changes(self) -> dict:
        """Get delta changes"""
        return self.delta

    def has_changes(self) -> bool:
        """Check if there are any delta changes"""
        return bool(self.delta)

    def to_dict(self) -> dict:
        """Convert device data to dictionary"""
        return {
            'device_id': self.device_id,
            'power': self.power,
            'mode': self.mode,
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'swing': self.swing,
            'fresh_air': self.fresh_air,
            'eco_mode': self.eco_mode,
            'sleep_mode': self.sleep_mode
        }