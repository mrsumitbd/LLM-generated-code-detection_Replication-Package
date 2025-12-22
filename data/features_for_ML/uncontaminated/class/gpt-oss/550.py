class TCL_SplitAC_DeviceData:
    """
    A lightweight container for a TCL Split AC device's state information.
    It stores the device identifier, the full AWS IoT Thing state, and any
    pending delta changes.  The class provides convenient accessors for
    common attributes such as power, mode, temperature, and fan speed.
    """

    def __init__(self, device_id: str, aws_thing_state: dict, delta: dict) -> None:
        self.device_id = device_id
        self.aws_thing_state = aws_thing_state or {}
        self.delta = delta or {}

    # ------------------------------------------------------------------
    # Generic helpers for nested dictionaries
    # ------------------------------------------------------------------
    @staticmethod
    def _get_nested(data: dict, keys: list, default=None):
        """Return a nested value from a dict using a list of keys."""
        for key in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(key, default)
        return data

    # ------------------------------------------------------------------
    # Reported state accessors
    # ------------------------------------------------------------------
    def get_reported(self, key: str, default=None):
        """Return a value from the reported state."""
        return self._get_nested(self.aws_thing_state, ["state", "reported", key], default)

    def get_desired(self, key: str, default=None):
        """Return a value from the desired state."""
        return self._get_nested(self.aws_thing_state, ["state", "desired", key], default)

    # ------------------------------------------------------------------
    # Delta accessors
    # ------------------------------------------------------------------
    def get_delta(self, key: str, default=None):
        """Return a value from the delta dictionary."""
        return self.delta.get(key, default)

    # ------------------------------------------------------------------
    # Convenience properties for common device attributes
    # ------------------------------------------------------------------
    @property
    def power(self):
        """Power status: 'ON' or 'OFF'."""
        return self.get_reported("power", "OFF")

    @property
    def mode(self):
        """Current operating mode (e.g., 'cool', 'heat', 'fan')."""
        return self.get_reported("mode", "unknown")

    @property
    def target_temperature(self):
        """Desired temperature setpoint."""
        return self.get_reported("targetTemperature", None)

    @property
    def current_temperature(self):
        """Measured indoor temperature."""
        return self.get_reported("currentTemperature", None)

    @property
    def fan_speed(self):
        """Fan speed setting (e.g., 'low', 'medium', 'high')."""
        return self.get_reported("fanSpeed", "unknown")

    @property
    def is_power_on(self):
        """True if the device is powered on."""
        return self.power.upper() == "ON"

    # ------------------------------------------------------------------
    # Representation helpers
    # ------------------------------------------------------------------
    def __repr__(self):
        return (
            f"<TCL_SplitAC_DeviceData id={self.device_id!r} "
            f"power={self.power!r} mode={self.mode!r} "
            f"targetTemp={self.target_temperature!r} fan={self.fan_speed!r}>"
        )

    def __str__(self):
        return (
            f"Device {self.device_id}: Power={self.power}, Mode={self.mode}, "
            f"Target Temp={self.target_temperature}, Fan={self.fan_speed}"
        )