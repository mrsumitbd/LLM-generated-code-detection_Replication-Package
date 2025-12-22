class Battery:
    """Battery class to represent a battery with its type, voltage, voltage ranges, state and percent os state of charge or discharge"""

    def __init__(self, config_dict: dict[str, Any]):
        self._battery_info = self.config_to_battery_info(config_dict)
        self._voltage = self._battery_info.voltage
        self._state = BatteryState.UNKNOWN
        self._percent = 0
        self._real_time_data = None

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        self._voltage = value

    @property
    def state(self) -> BatteryState:
        return self._state

    @property
    def percent(self) -> int:
        return self._percent

    @property
    def range(self) -> BatteryRange:
        return self._battery_info.range

    @property
    def soc(self) -> float:
        if self._battery_info.range.max_voltage == self._battery_info.range.min_voltage:
            return 0.0
        return (self._voltage - self._battery_info.range.min_voltage) / (
            self._battery_info.range.max_voltage - self._battery_info.range.min_voltage
        ) * 100

    @property
    def sod(self) -> float:
        return 100 - self.soc

    @property
    def cvr(self) -> float:
        if self._battery_info.range.max_voltage == self._battery_info.range.min_voltage:
            return 0.0
        return (self._voltage - self._battery_info.range.min_voltage) / (
            self._battery_info.range.max_voltage - self._battery_info.range.min_voltage
        ) * 100

    @property
    def dvr(self) -> float:
        return 100 - self.cvr

    @property
    def is_dvr(self) -> bool:
        return self._state == BatteryState.DISCHARGING

    @property
    def is_cvr(self) -> bool:
        return self._state == BatteryState.CHARGING

    @property
    def is_soc(self) -> bool:
        return self._state == BatteryState.CHARGING

    @property
    def is_sod(self) -> bool:
        return self._state == BatteryState.DISCHARGING

    def update(self, real_time_data: BM6RealTimeData, voltage: float):
        self._real_time_data = real_time_data
        self._voltage = voltage
        self._update_state()
        self._update_percent()

    def _update_state(self):
        if self._real_time_data is None:
            self._state = BatteryState.UNKNOWN
        else:
            self._state = self._bm6_status_to_battery_state(self._real_time_data.state)

    def _bm6_status_to_battery_state(self, state: BM6RealTimeState) -> BatteryState:
        if state == BM6RealTimeState.CHARGING:
            return BatteryState.CHARGING
        elif state == BM6RealTimeState.DISCHARGING:
            return BatteryState.DISCHARGING
        elif state == BM6RealTimeState.IDLE:
            return BatteryState.IDLE
        else:
            return BatteryState.UNKNOWN

    def _update_percent(self):
        self._percent = int(round(self.soc))
        self._percent = max(0, min(100, self._percent))

    def get_diagnostic_data(self) -> dict[str, Any]:
        return {
            "battery_info": {
                "type": self._battery_info.type,
                "voltage": self._battery_info.voltage,
                "range": {
                    "min_voltage": self._battery_info.range.min_voltage,
                    "max_voltage": self._battery_info.range.max_voltage,
                },
            },
            "current_voltage": self._voltage,
            "state": self._state.value,
            "percent": self._percent,
            "soc": round(self.soc, 2),
            "sod": round(self.sod, 2),
            "cvr": round(self.cvr, 2),
            "dvr": round(self.dvr, 2),
        }

    @staticmethod
    def config_to_battery_info(config_dict: dict[str, Any]) -> BatteryInfo:
        battery_type = config_dict.get("type", "Unknown")
        voltage = config_dict.get("voltage", 0.0)
        min_voltage = config_dict.get("min_voltage", 0.0)
        max_voltage = config_dict.get("max_voltage", 0.0)
        
        battery_range = BatteryRange(min_voltage=min_voltage, max_voltage=max_voltage)
        return BatteryInfo(type=battery_type, voltage=voltage, range=battery_range)

    @staticmethod
    def percent_to_icon(percent: int) -> str:
        if percent >= 90:
            return "🔋"
        elif percent >= 70:
            return "🔋"
        elif percent >= 50:
            return "🔋"
        elif percent >= 30:
            return "🔋"
        elif percent >= 10:
            return "🪫"
        else:
            return "🪫"