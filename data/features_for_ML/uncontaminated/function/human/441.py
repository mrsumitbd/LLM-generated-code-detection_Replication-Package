from .const import (
    CONF_BLUETOOTH_SCANNER,
    CONF_TEMPERATURE_OFFSET,
    CONF_TEMPERATURE_UNIT,
    CONF_VOLTAGE_OFFSET,
    DEFAULT_TEMPERATURE_OFFSET,
    DEFAULT_TEMPERATURE_UNIT,
    DEFAULT_VOLTAGE_OFFSET,
    DOMAIN,
    CONF_DEVICE_ADDRESS,
    CONF_CUSTOM_DVR_MIN,
    CONF_CUSTOM_DVR_MAX,
    CONF_CUSTOM_CVR_MIN,
    CONF_CUSTOM_CVR_MAX,
    CONF_CUSTOM_SOD_MIN,
    CONF_CUSTOM_SOD_MAX,
    CONF_CUSTOM_SOC_MIN,
    CONF_CUSTOM_SOC_MAX,
    CONF_BATTERY_VOLTAGE,
    CONF_BATTERY_TYPE,
    CONF_STATE_ALGORITHM,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    MIN_UPDATE_INTERVAL,
    ERROR_MAX_LESS_THAN_MIN,
    ERROR_CVR_LESS_THAN_DVR,
    ERROR_SOC_LESS_THAN_SOD,
    TRANSLATION_KEY_BATTERY_STATE_ALGORITHM,
    TRANSLATION_KEY_BATTERY_TYPE,
    TRANSLATION_KEY_BATTERY_VOLTAGE,
    TRANSLATION_KEY_BLUETOOTH_SCANNER,
)
from .battery import (
    battery_voltage_ranges,
    BatteryType,
    BatteryVoltage,
    BatteryStateAlgorithm,
    Battery,
)
from typing import TYPE_CHECKING, Any

def validate_custom_voltage(
    data: dict[str, Any], errors: dict[str, str]
) -> dict[str, str]:
    """Validate custom voltage settings."""
    battery_info = Battery.config_to_battery_info(data)
    if battery_info.type == BatteryType.Custom:
        if not battery_info.custom.dvr.is_valid:
            errors[CONF_CUSTOM_DVR_MAX] = ERROR_MAX_LESS_THAN_MIN
        if not battery_info.custom.cvr.is_valid:
            errors[CONF_CUSTOM_CVR_MAX] = ERROR_MAX_LESS_THAN_MIN
        if not battery_info.custom.sod.is_valid:
            errors[CONF_CUSTOM_SOD_MAX] = ERROR_MAX_LESS_THAN_MIN
        if not battery_info.custom.soc.is_valid:
            errors[CONF_CUSTOM_SOC_MAX] = ERROR_MAX_LESS_THAN_MIN
        if not battery_info.custom.is_dvr_less_cvr:
            errors[CONF_CUSTOM_DVR_MAX] = ERROR_CVR_LESS_THAN_DVR
        if not battery_info.custom.is_sod_less_soc:
            errors[CONF_CUSTOM_SOD_MAX] = ERROR_SOC_LESS_THAN_SOD
    return errors