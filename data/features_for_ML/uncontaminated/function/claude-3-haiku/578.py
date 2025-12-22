def choose_device(devices: list) -> dict | None:
    if not devices:
        return None

    devices.sort(key=lambda x: x['score'], reverse=True)
    return devices[0]