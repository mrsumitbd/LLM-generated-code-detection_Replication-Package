from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


class BatteryState(Enum):
    UNKNOWN = auto()
    CHARGING = auto()
    DISCHARGING = auto()
    FULL = auto()
    EMPTY = auto()


class BatteryRange(Enum):
    UNKNOWN = auto()
    FULL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    EMPTY = auto()


class BM6RealTimeState(Enum):
    UNKNOWN = auto()
    CHARGING = auto()
    DISCHARGING = auto()
    FULL = auto()
    EMPTY = auto()


@dataclass
class BM6RealTimeData:
    state: BM6RealTimeState


@dataclass
class BatteryInfo:
    type: str
    voltage_min: float
    voltage_max: float
    cvr_min: Optional[float] = None
    cvr_max: Optional[float] = None
    dvr_min: Optional[float] = None
    dvr_max: Optional[float] = None
    soc_min: Optional[float] = None
    soc_max: Optional[float] = None
    sod_min: Optional[float] = None
    sod_max: Optional[float] = None


class Battery:
    """Battery class to represent a battery with its type, voltage, voltage ranges, state and percent of state of charge or discharge"""

    def __init__(self, config_dict: Dict[str, Any]):
        self._config = config_dict
        self._voltage: float = 0.0
        self._state: BatteryState = BatteryState.UNKNOWN
        self._percent: int = 0
        self._range: BatteryRange = BatteryRange.UNKNOWN

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        self._voltage = value
        self._update_state()
        self._update_percent()

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
        if self._config.get("soc_min") is None or self._config.get("soc_max") is None:
            return 0.0
        return (self._voltage - self._config["soc_min"]) / (
            self._config["soc_max"] - self._config["soc_min"]
        )

    @property
    def sod(self) -> float:
        if self._config.get("sod_min") is None or self._config.get("sod_max") is None:
            return 0.0
        return (self._voltage - self._config["sod_min"]) / (
            self._config["sod_max"] - self._config["sod_min"]
        )

    @property
    def cvr(self) -> float:
        if self._config.get("cvr_min") is None or self._config.get("cvr_max") is None:
            return 0.0
        return (self._voltage - self._config["cvr_min"]) / (
            self._config["cvr_max"] - self._config["cvr_min"]
        )

    @property
    def dvr(self) -> float:
        if self._config.get("dvr_min") is None or self._config.get("dvr_max") is None:
            return 0.0
        return (self._voltage - self._config["dvr_min"]) / (
            self._config["dvr_max"] - self._config["dvr_min"]
        )

    @property
    def is_dvr(self) -> bool:
        return (
            self._config.get("dvr_min") is not None
            and self._config.get("dvr_max") is not None
            and self._config["dvr_min"] <= self._voltage <= self._config["dvr_max"]
        )

    @property
    def is_cvr(self) -> bool:
        return (
            self._config.get("cvr_min") is not None
            and self._config.get("cvr_max") is not None
            and self._config["cvr_min"] <= self._voltage <= self._config["cvr_max"]
        )

    @property
    def is_soc(self) -> bool:
        return (
            self._config.get("soc_min") is not None
            and self._config.get("soc_max") is not None
            and self._config["soc_min"] <= self._voltage <= self._config["soc_max"]
        )

    @property
    def is_sod(self) -> bool:
        return (
            self._config.get("sod_min") is not None
            and self._config.get("sod_max") is not None
            and self._config["sod_min"] <= self._voltage <= self._config["sod_max"]
        )

    def update(self, real_time_data: BM6RealTimeData, voltage: float):
        self.voltage = voltage
        self._state = self._bm6_status_to_battery_state(real_time_data.state)

    def _update_state(self):
        if self._config.get("voltage_min") is None or self._config.get("voltage_max") is None:
            self._state = BatteryState.UNKNOWN
            return
        if self._voltage >= self._config["voltage_max"]:
            self._state = BatteryState.FULL
        elif self._voltage <= self._config["voltage_min"]:
            self._state = BatteryState.EMPTY
        else:
            self._state = BatteryState.UNKNOWN

    def _bm6_status_to_battery_state(self, state: BM6RealTimeState) -> BatteryState:
        mapping = {
            BM6RealTimeState.UNKNOWN: BatteryState.UNKNOWN,
            BM6RealTimeState.CHARGING: BatteryState.CHARGING,
            BM6RealTimeState.DISCHARGING: BatteryState.DISCHARGING,
            BM6RealTimeState.FULL: BatteryState.FULL,
            BM6RealTimeState.EMPTY: BatteryState.EMPTY,
        }
        return mapping.get(state, BatteryState.UNKNOWN)

    def _update_percent(self):
        if self._config.get("voltage_min") is None or self._config.get("voltage_max") is None:
            self._percent = 0
            return
        v_min = self._config["voltage_min"]
        v_max = self._config["voltage_max"]
        if self._voltage <= v_min:
            self._percent = 0
        elif self._voltage >= v_max:
            self._percent = 100
        else:
            self._percent = int(
                ((self._voltage - v_min) / (v_max - v_min)) * 100
            )
        # Determine range
        if self._percent >= 90:
            self._range = BatteryRange.FULL
        elif self._percent >= 70:
            self._range = BatteryRange.HIGH
        elif self._percent >= 30:
            self._range = BatteryRange.MEDIUM
        elif self._percent >= 10:
            self._range = BatteryRange.LOW
        else:
            self._range = BatteryRange.EMPTY

    def get_diagnostic_data(self) -> Dict[str, Any]:
        return {
            "voltage": self._voltage,
            "state": self._state.name,
            "percent": self._percent,
            "range": self._range.name,
            "soc": self.soc,
            "sod": self.sod,
            "cvr": self.cvr,
            "dvr": self.dvr,
            "is_cvr": self.is_cvr,
            "is_dvr": self.is_dvr,
            "is_soc": self.is_soc,
            "is_sod": self.is_sod,
        }

    @staticmethod
    def config_to_battery_info(config_dict: Dict[str, Any]) -> BatteryInfo:
        return BatteryInfo(
            type=config_dict.get("type", "unknown"),
            voltage_min=config_dict.get("voltage_min", 0.0),
            voltage_max=config_dict.get("voltage_max", 0.0),
            cvr_min=config_dict.get("cvr_min"),
            cvr_max=config_dict.get("cvr_max"),
            dvr_min=config_dict.get("dvr_min"),
            dvr_max=config_dict.get("dvr_max"),
            soc_min=config_dict.get("soc_min"),
            soc_max=config_dict.get("soc_max"),
            sod_min=config_dict.get("sod_min"),
            sod_max=config_dict.get("sod_max"),
        )

    @staticmethod
    def percent_to_icon(percent: int) -> str:
        if percent >= 90:
            return "🔋"
        if percent >= 70:
            return "🟢"
        if percent >= 30:
            return "🟡"
        if percent >= 10:
            return "🟠"
        return "🔴"