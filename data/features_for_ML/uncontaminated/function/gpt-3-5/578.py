def choose_device(devices: list) -> dict | None:
    if not devices:
        return None
    return devices[0]