from typing import Any, Dict

class Battery:
    """Battery class to represent a battery with its type, voltage, voltage ranges, state and percent os state of charge or discharge"""

    def __init__(self, config_dict: Dict[str, Any]):
        pass

    @property
    def voltage(self) -> float:
        pass

    @voltage.setter
    def voltage(self, value: float):
        pass

    @property
    def state(self) -> BatteryState:
        pass

    @property
    def percent(self) -> int:
        pass

    @property
    def range(self) -> BatteryRange:
        pass

    @property
    def soc(self) -> float:
        pass

    @property
    def sod(self) -> float:
        pass

    @property
    def cvr(self) -> float:
        pass

    @property
    def dvr(self) -> float:
        pass

    @property
    def is_dvr(self) -> bool:
        pass

    @property
    def is_cvr(self) -> bool:
        pass

    @property
    def is_soc(self) -> bool:
        pass

    @property
    def is_sod(self) -> bool:
        pass

    def update(self, real_time_data: BM6RealTimeData, voltage: float):
        pass

    def _update_state(self):
        pass

    def _bm6_status_to_battery_state(self, state: BM6RealTimeState) -> BatteryState:
        pass

    def _update_percent(self):
        pass

    def get_diagnostic_data(self) -> Dict[str, Any]:
        pass

    @staticmethod
    def config_to_battery_info(config_dict: Dict[str, Any]) -> BatteryInfo:
        pass

    @staticmethod
    def percent_to_icon(percent: int) -> str:
        pass