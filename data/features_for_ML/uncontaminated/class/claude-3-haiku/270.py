from typing import Any
from enum import Enum

class BatteryState(Enum):
    CHARGING = 'Charging'
    DISCHARGING = 'Discharging'
    FULL = 'Full'
    EMPTY = 'Empty'

class BatteryRange(Enum):
    NORMAL = 'Normal'
    CRITICAL = 'Critical'
    UNKNOWN = 'Unknown'

class BM6RealTimeState(Enum):
    CHARGING = 'Charging'
    DISCHARGING = 'Discharging'
    FULL = 'Full'
    EMPTY = 'Empty'

class BM6RealTimeData:
    def __init__(self, state: BM6RealTimeState, soc: float, sod: float, cvr: float, dvr: float):
        self.state = state
        self.soc = soc
        self.sod = sod
        self.cvr = cvr
        self.dvr = dvr

class BatteryInfo:
    def __init__(self, battery_type: str, voltage_range: tuple[float, float], capacity: float):
        self.battery_type = battery_type
        self.voltage_range = voltage_range
        self.capacity = capacity

class Battery:
    """Battery class to represent a battery with its type, voltage, voltage ranges, state and percent os state of charge or discharge"""

    def __init__(self, config_dict: dict[str, Any]):
        self._battery_info = self.config_to_battery_info(config_dict)
        self._voltage = config_dict['voltage']
        self._state = BatteryState.EMPTY
        self._percent = 0
        self._range = BatteryRange.UNKNOWN

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        self._voltage = value
        self._update_state()

    @property
    def state(self) -> BatteryState:
        return self._state

    @property
    def percent(self) -> int:
        return self._percent

    @property
    def range(self) -> BatteryRange:
        return self._range

    @property
    def soc(self) -> float:
        return self._battery_info.capacity * (self._percent / 100)

    @property
    def sod(self) -> float:
        return self._battery_info.capacity * ((100 - self._percent) / 100)

    @property
    def cvr(self) -> float:
        return self._battery_info.voltage_range[1]

    @property
    def dvr(self) -> float:
        return self._battery_info.voltage_range[0]

    @property
    def is_dvr(self) -> bool:
        return self.voltage < self.dvr

    @property
    def is_cvr(self) -> bool:
        return self.voltage > self.cvr

    @property
    def is_soc(self) -> bool:
        return self._percent == 100

    @property
    def is_sod(self) -> bool:
        return self._percent == 0

    def update(self, real_time_data: BM6RealTimeData, voltage: float):
        self._voltage = voltage
        self.update_state(real_time_data)

    def _update_state(self):
        self._state = self._bm6_status_to_battery_state(self._battery_info.state)
        self._update_percent()

    def _bm6_status_to_battery_state(self, state: BM6RealTimeState) -> BatteryState:
        state_map = {
            BM6RealTimeState.CHARGING: BatteryState.CHARGING,
            BM6RealTimeState.DISCHARGING: BatteryState.DISCHARGING,
            BM6RealTimeState.FULL: BatteryState.FULL,
            BM6RealTimeState.EMPTY: BatteryState.EMPTY,
        }
        return state_map[state]

    def _update_percent(self):
        if self.is_soc:
            self._percent = 100
        elif self.is_sod:
            self._percent = 0
        else:
            self._percent = int((self.voltage - self.dvr) / (self.cvr - self.dvr) * 100)

    def get_diagnostic_data(self) -> dict[str, Any]:
        return {
            'battery_type': self._battery_info.battery_type,
            'voltage': self.voltage,
            'state': self.state.value,
            'percent': self.percent,
            'range': self.range.value,
            'soc': self.soc,
            'sod': self.sod,
            'cvr': self.cvr,
            'dvr': self.dvr,
            'is_dvr': self.is_dvr,
            'is_cvr': self.is_cvr,
            'is_soc': self.is_soc,
            'is_sod': self.is_sod,
        }

    @staticmethod
    def config_to_battery_info(config_dict: dict[str, Any]) -> BatteryInfo:
        return BatteryInfo(
            battery_type=config_dict['battery_type'],
            voltage_range=(config_dict['voltage_range_min'], config_dict['voltage_range_max']),
            capacity=config_dict['capacity'],
        )

    @staticmethod
    def percent_to_icon(percent: int) -> str:
        if percent >= 80:
            return '🔋'
        elif percent >= 60:
            return '🔋'
        elif percent >= 40:
            return '🔋'
        elif percent >= 20:
            return '🔋'
        else:
            return '🔋'