def get_optimal_device() -> DeviceInfo:
    devices = detect_available_devices()
    return devices[0] if devices else DeviceInfo(device_type="cpu", name="CPU")