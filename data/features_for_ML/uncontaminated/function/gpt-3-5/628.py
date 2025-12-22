from typing import Union

def sensor_update_to_bluetooth_data_update(
    sensor_update: SensorUpdate,
) -> PassiveBluetoothDataUpdate[Union[float, None]]:
    return PassiveBluetoothDataUpdate(
        timestamp=sensor_update.timestamp,
        data=sensor_update.data if sensor_update.data is not None else None,
    )