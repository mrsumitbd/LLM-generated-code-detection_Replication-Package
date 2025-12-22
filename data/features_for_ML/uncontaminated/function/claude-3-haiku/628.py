def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[float | None]:
    """Convert a sensor update to a bluetooth data update."""
    return PassiveBluetoothDataUpdate(
        timestamp=sensor_update.timestamp,
        device_id=sensor_update.device_id,
        data=sensor_update.value,
    )