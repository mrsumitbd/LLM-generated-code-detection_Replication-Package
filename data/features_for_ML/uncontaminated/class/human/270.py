from .const import (
    CONF_CUSTOM_DVR_MIN,
    CONF_CUSTOM_DVR_MAX,
    CONF_CUSTOM_CVR_MIN,
    CONF_CUSTOM_CVR_MAX,
    CONF_CUSTOM_SOC_MIN,
    CONF_CUSTOM_SOC_MAX,
    CONF_CUSTOM_SOD_MIN,
    CONF_CUSTOM_SOD_MAX,
    CONF_BATTERY_VOLTAGE,
    CONF_BATTERY_TYPE,
    CONF_STATE_ALGORITHM,
)
from .bm6_connect import BM6RealTimeData, BM6RealTimeState
from typing import Any

class Battery:
    """Battery class to represent a battery with its type, voltage, voltage ranges, state and percent os state of charge or discharge"""

    def __init__(self, config_dict: dict[str, Any]):
        self.info: BatteryInfo = self.config_to_battery_info(config_dict)
        self._voltage: float = 0.0
        self._state: BatteryState = BatteryState.Idle
        self._percent: int = 0

    @property
    def voltage(self) -> float:
        """Get the current voltage of the battery."""
        return self._voltage

    @voltage.setter
    def voltage(self, value: float):
        """Set the current voltage of the battery and update state and percent."""
        self._voltage = value
        self._update_state()
        self._update_percent()

    @property
    def state(self) -> BatteryState:
        """Get the current state of the battery."""
        return self._state

    @property
    def percent(self) -> int:
        """Get the current percentage of the battery."""
        return self._percent

    @property
    def range(self) -> BatteryRange:
        """Get the voltage ranges of the battery."""
        if self.info.type == BatteryType.Custom:
            return self.info.custom
        else:
            return battery_voltage_ranges[(self.info.type, self.info.voltage)]

    @property
    def soc(self) -> float:
        """Calculate the State of Charge (SoC) as a percentage."""
        return self.range.soc.calc_percent(self._voltage)

    @property
    def sod(self) -> float:
        """Calculate the State of Discharge (SoD) as a percentage."""
        return self.range.sod.calc_percent(self._voltage)

    @property
    def cvr(self) -> float:
        """Calculate the Charging Voltage Range (CVR) as a percentage."""
        return self.range.cvr.calc_percent(self._voltage)

    @property
    def dvr(self) -> float:
        """Calculate the Discharging Voltage Range (DVR) as a percentage."""
        return self.range.dvr.calc_percent(self._voltage)

    @property
    def is_dvr(self) -> bool:
        """Check if the current voltage is within the Discharging Voltage Range (DVR)."""
        return self.range.dvr.in_range(self._voltage)

    @property
    def is_cvr(self) -> bool:
        """Check if the current voltage is within the Charging Voltage Range (CVR)."""
        return self.range.cvr.in_range(self._voltage)

    @property
    def is_soc(self) -> bool:
        """Check if the current voltage is within the State of Charge (SoC) range."""
        return self.range.soc.in_range(self._voltage)

    @property
    def is_sod(self) -> bool:
        """Check if the current voltage is within the State of Discharge (SoD) range."""
        return self.range.sod.in_range(self._voltage)

    def update(self, real_time_data: BM6RealTimeData, voltage: float):
        """Set the real-time data of the battery."""
        self._voltage = voltage
        if self.info.state_algorithm == BatteryStateAlgorithm.By_Device:
            self._percent = real_time_data.Percent
            self._state = self._bm6_status_to_battery_state(real_time_data.State)
        else:
            self._update_percent()
            self._update_state()

    def _update_state(self):
        """Update the state of the battery based on its voltage."""
        if self.info.state_algorithm == BatteryStateAlgorithm.By_Device:
            return
        if self._voltage is None:
            self._state = None
        if self._voltage < self.range.dvr.min:
            self._state = BatteryState.UnderVoltage
        elif self._voltage > self.range.cvr.max:
            self._state = BatteryState.OverVoltage
        elif (self.info.state_algorithm == BatteryStateAlgorithm.SoC_SoD and self.is_sod) or (
            self.info.state_algorithm == BatteryStateAlgorithm.CVR_DVR and self.is_dvr
        ):
            self._state = BatteryState.Discharging
        elif (self.info.state_algorithm == BatteryStateAlgorithm.SoC_SoD and self.is_soc) or (
            self.info.state_algorithm == BatteryStateAlgorithm.CVR_DVR and self.is_cvr
        ):
            self._state = BatteryState.Charging
        else:
            self._state = BatteryState.Idle

    def _bm6_status_to_battery_state(self, state: BM6RealTimeState) -> BatteryState:
        """Convert BM6 real-time status to BatteryState."""
        state_mapping = {
            BM6RealTimeState.BatteryOk: BatteryState.Ok,
            BM6RealTimeState.LowVoltage: BatteryState.LowVoltage,
            BM6RealTimeState.Charging: BatteryState.Charging,
        }
        return state_mapping.get(state, BatteryState.Unknown)

    def _update_percent(self):
        """Get the percentage of SoC or SoD or CVR or DVR depending on the algorithm and current state."""
        if self.info.state_algorithm == BatteryStateAlgorithm.By_Device:
            return
        elif self.info.state_algorithm == BatteryStateAlgorithm.SoC_SoD:
            if self.is_soc:
                self._percent = self.soc
            elif self.is_sod:
                self._percent = self.sod
            elif self.state == BatteryState.Idle:
                self._percent = 100
            else:
                self._percent = 0
        elif self.info.state_algorithm == BatteryStateAlgorithm.CVR_DVR:
            if self.is_cvr:
                self._percent = self.cvr
            elif self.is_dvr:
                self._percent = self.dvr
            elif self.state == BatteryState.Idle:
                self._percent = 100
            else:
                self._percent = 0
        else:
            self._percent = 0

    def get_diagnostic_data(self) -> dict[str, Any]:
        """Get diagnostic data for the battery."""
        return {
            "voltage": self.voltage,
            "state": self.state.value,
            "percent": self.percent,
            "info": self.info.get_diagnostic_data(),
        }

    @staticmethod
    def config_to_battery_info(config_dict: dict[str, Any]) -> BatteryInfo:
        voltage = config_dict.get(CONF_BATTERY_VOLTAGE)
        if voltage not in BatteryVoltage._value2member_map_:
            raise ValueError(f"Invalid battery voltage: {voltage}")

        battery_type = config_dict.get(CONF_BATTERY_TYPE)
        if battery_type not in BatteryType._value2member_map_:
            raise ValueError(f"Invalid battery type: {battery_type}")

        state_algorithm = config_dict.get(CONF_STATE_ALGORITHM)
        if state_algorithm not in BatteryStateAlgorithm._value2member_map_:
            raise ValueError(f"Invalid battery state algorithm: {state_algorithm}")

        return BatteryInfo(
            voltage=BatteryVoltage(voltage),
            type=BatteryType(battery_type),
            custom=BatteryRange(
                dvr=VoltageRange(
                    min=config_dict.get(CONF_CUSTOM_DVR_MIN),
                    max=config_dict.get(CONF_CUSTOM_DVR_MAX),
                ),
                cvr=VoltageRange(
                    min=config_dict.get(CONF_CUSTOM_CVR_MIN),
                    max=config_dict.get(CONF_CUSTOM_CVR_MAX),
                ),
                soc=VoltageRange(
                    min=config_dict.get(CONF_CUSTOM_SOC_MIN),
                    max=config_dict.get(CONF_CUSTOM_SOC_MAX),
                ),
                sod=VoltageRange(
                    min=config_dict.get(CONF_CUSTOM_SOD_MIN),
                    max=config_dict.get(CONF_CUSTOM_SOD_MAX),
                ),
            ),
            state_algorithm=BatteryStateAlgorithm(state_algorithm),
        )

    @staticmethod
    def percent_to_icon(percent: int) -> str:
        """Get the icon based on the percentage."""
        if percent is None:
            return "mdi:battery"
        if percent < 10:
            return "mdi:battery-outline"
        if percent < 20:
            return "mdi:battery-10"
        if percent < 30:
            return "mdi:battery-20"
        if percent < 40:
            return "mdi:battery-30"
        if percent < 50:
            return "mdi:battery-40"
        if percent < 60:
            return "mdi:battery-50"
        if percent < 70:
            return "mdi:battery-60"
        if percent < 80:
            return "mdi:battery-70"
        if percent < 90:
            return "mdi:battery-80"
        if percent < 100:
            return "mdi:battery-90"
        return "mdi:battery"