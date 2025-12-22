from dataclasses import fields
from typing import Any

def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[float | None]:
    """
    Convert a SensorUpdate instance into a PassiveBluetoothDataUpdate instance.
    The conversion is performed by matching field names between the two dataclasses.
    If a PassiveBluetoothDataUpdate field is named ``device_id`` and the
    SensorUpdate has a ``sensor_id`` field, the value is copied accordingly.
    """
    # Build keyword arguments for the PassiveBluetoothDataUpdate constructor
    kwargs: dict[str, Any] = {}
    for f in fields(PassiveBluetoothDataUpdate):
        # Direct match
        if hasattr(sensor_update, f.name):
            kwargs[f.name] = getattr(sensor_update, f.name)
        # Special case: map sensor_id → device_id
        elif f.name == "device_id" and hasattr(sensor_update, "sensor_id"):
            kwargs[f.name] = getattr(sensor_update, "sensor_id")

    return PassiveBluetoothDataUpdate(**kwargs)