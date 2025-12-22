from .calculations import try_get_value

class TCL_SplitAC_Fresh_Air_DeviceData:
    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.power_switch                       = int(try_get_value(delta, aws_thing_state, "powerSwitch", -1))
        self.beep_switch                        = int(try_get_value(delta, aws_thing_state, "beepSwitch", -1))
        self.target_temperature                 = float(try_get_value(delta, aws_thing_state, "targetTemperature", -1))
        self.current_temperature                = float(try_get_value(delta, aws_thing_state, "currentTemperature", -1))
        self.internal_unit_coil_temperature     = float(try_get_value(delta, aws_thing_state, "internalUnitCoilTemperature", -1))
        self.work_mode                          = int(try_get_value(delta, aws_thing_state, "workMode", -1))
        self.vertical_direction                 = int(try_get_value(delta, aws_thing_state, "verticalDirection", -1))
        self.horizontal_direction               = int(try_get_value(delta, aws_thing_state, "horizontalDirection", -1))
        self.wind_speed_auto_switch             = int(try_get_value(delta, aws_thing_state, "windSpeedAutoSwitch", -1))
        self.wind_speed_7_gear                  = int(try_get_value(delta, aws_thing_state, "windSpeed7Gear", -1))
        self.new_wind_switch                    = int(try_get_value(delta, aws_thing_state, "newWindSwitch", -1))
        self.new_wind_auto_switch               = int(try_get_value(delta, aws_thing_state, "newWindAutoSwitch", -1))
        self.new_wind_strength                  = int(try_get_value(delta, aws_thing_state, "newWindStrength", -1))
        self.soft_wind                          = int(try_get_value(delta, aws_thing_state, "softWind", -1))
        self.generator_mode                     = int(try_get_value(delta, aws_thing_state, "generatorMode", -1))
        self.sleep                              = int(try_get_value(delta, aws_thing_state, "sleep", -1))
        self.eco                                = int(try_get_value(delta, aws_thing_state, "ECO", -1))
        self.healthy                            = int(try_get_value(delta, aws_thing_state, "healthy", -1))
        self.anti_moldew                        = int(try_get_value(delta, aws_thing_state, "antiMoldew", -1))
        self.self_clean                         = int(try_get_value(delta, aws_thing_state, "selfClean", -1))
        self.screen                             = int(try_get_value(delta, aws_thing_state, "screen", -1))
        self.light_sense                        = int(try_get_value(delta, aws_thing_state, "lightSense", -1))
        self.external_unit_coil_temperature     = float(try_get_value(delta, aws_thing_state, "externalUnitCoilTemperature", -1))
        self.external_unit_temperature          = float(try_get_value(delta, aws_thing_state, "externalUnitTemperature", -1))
        self.external_unit_exhaust_temperature  = float(try_get_value(delta, aws_thing_state, "externalUnitExhaustTemperature", -1))
        self.lower_temperature_limit            = int(try_get_value(delta, aws_thing_state, "lowerTemperatureLimit", 16))
        self.upper_temperature_limit            = int(try_get_value(delta, aws_thing_state, "upperTemperatureLimit", 31))
        self.tvoc_level                         = int(try_get_value(delta, aws_thing_state, "sensorTVOC", {"level":-1, "value":0.1}).get("level", -1))
        self.tvoc_value                         = float(try_get_value(delta, aws_thing_state, "sensorTVOC", {"level":-1, "value":0.1}).get("value", 0.1))

    device_id: str
    power_switch: int | bool
    beep_switch: int | bool
    target_temperature: float
    current_temperature: float
    internal_unit_coil_temperature: float
    external_unit_coil_temperature: float
    external_unit_exhaust_temperature: float
    external_unit_temperature: float
    vertical_direction: int
    horizontal_direction: int
    sleep: int
    healthy: int
    eco: int
    anti_moldew: int
    self_clean: int
    screen: int
    wind_speed_auto_switch: int
    wind_speed_7_gear: int
    new_wind_switch: int
    new_wind_auto_switch: int
    new_wind_strength: int
    soft_wind: int
    generator_mode: int
    light_sense: int
    upper_temperature_limit: int
    lower_temperature_limit: int
    tvoc_level: int
    tvoc_value: float