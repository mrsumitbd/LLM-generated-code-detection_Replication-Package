def fluid_field_weights_gravity(value):
    if value < 0:
        return "Invalid input"
    elif value <= 1000:
        return value * 9.81
    else:
        return value * 9.81 * 0.9