def choose_device(devices: list) -> dict | None:
    print_select_message(devices)
    try:
        selected_device = int(input("\n➡️  Select your device (1–{}): ".format(len(devices))))
        if 1 <= selected_device <= len(devices):
            return devices[selected_device - 1]
        else:
            print("❌ Invalid number. Please select a valid device index.\n")
            return choose_device(devices)
    except ValueError:
        print("⚠️  Please enter a number corresponding to a device.\n")
        return choose_device(devices)