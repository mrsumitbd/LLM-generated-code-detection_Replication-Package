def flow_initial_velocity_toggle(value):
    if value == "ON":
        return "OFF"
    elif value == "OFF":
        return "ON"
    else:
        return "Invalid value"