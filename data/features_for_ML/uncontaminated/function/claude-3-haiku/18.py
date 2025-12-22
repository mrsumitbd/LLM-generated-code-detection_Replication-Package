from typing import NamedTuple

class DeviceInfo(NamedTuple):
    device_id: str
    device_name: str
    device_type: str
    device_performance: float

import os
import psutil

def get_optimal_device() -> DeviceInfo:
    devices = []
    for device in psutil.sensors_temperatures():
        for sensor in device.temperatures:
            devices.append(DeviceInfo(
                device_id=sensor.label,
                device_name=device.label,
                device_type='CPU',
                device_performance=psutil.cpu_freq().current
            ))

    for device in psutil.disk_partitions():
        if 'cdrom' not in device.opts:
            devices.append(DeviceInfo(
                device_id=device.device,
                device_name=device.mountpoint,
                device_type='Storage',
                device_performance=psutil.disk_usage(device.mountpoint).percent
            ))

    for device in psutil.net_if_stats():
        devices.append(DeviceInfo(
            device_id=device,
            device_name=device,
            device_type='Network',
            device_performance=psutil.net_if_stats()[device].speed
        ))

    return max(devices, key=lambda x: x.device_performance)