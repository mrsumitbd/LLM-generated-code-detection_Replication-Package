from .const import (
    DEBUG_ENABLED,
    DOMAIN,
    DOMAIN_DATA_MANAGERS,
    FULL_OPTIONS_SCHEMA,
    SC_CONF_NAME,
    TARGET_COVER_ENTITY_ID,
    VERSION,
    YAML_CONFIG_SCHEMA,
    LockState,
    MovementRestricted,
    SCDawnInput,
    SCDynamicInput,
    SCFacadeConfig,
    SCShadowInput,
    ShutterState,
    ShutterType,
)

class SCDynamicInputConfiguration:
    """Define defaults for dynamic configuration."""

    def __init__(self) -> None:
        """Define defaults for dynamic configuration."""
        self.brightness: float = 5000.0
        self.brightness_dawn: float = -1.0
        self.sun_elevation: float = 45.0
        self.sun_azimuth: float = 180.0
        self.shutter_current_height: float = -1.0
        self.shutter_current_angle: float = -1.0
        self.lock_integration: bool = False
        self.lock_integration_with_position: bool = False
        self.lock_height: float = 0.0
        self.lock_angle: float = 0.0
        self.movement_restriction_height: MovementRestricted = MovementRestricted.NO_RESTRICTION
        self.movement_restriction_angle: MovementRestricted = MovementRestricted.NO_RESTRICTION