def flow_initial_velocity_toggle(value):
    if value < 0:
        return 0
    elif value > 100:
        return 100
    else:
        return value