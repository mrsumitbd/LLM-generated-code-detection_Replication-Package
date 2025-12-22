def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[float | None]:
    """Convert a sensor update to a bluetooth data update."""
    return PassiveBluetoothDataUpdate(
        devices={
            sensor_update.device_id: DeviceUpdate(
                unique_id=sensor_update.device_id,
                manufacturer_data=sensor_update.manufacturer_data,
                advertisement_data=sensor_update.advertisement_data,
                rssi=sensor_update.rssi,
                tx_power=sensor_update.tx_power,
                local_name=sensor_update.local_name,
            )
        },
        source=sensor_update.source,
    )