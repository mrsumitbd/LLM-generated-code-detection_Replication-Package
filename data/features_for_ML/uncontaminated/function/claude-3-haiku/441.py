def validate_custom_voltage(
    data: dict[str, Any], errors: dict[str, str]
) -> dict[str, str]:
    """Validate custom voltage settings."""
    if 'custom_voltage' not in data:
        errors['custom_voltage'] = 'Custom voltage settings are required.'
    else:
        custom_voltage = data['custom_voltage']
        if not isinstance(custom_voltage, dict):
            errors['custom_voltage'] = 'Custom voltage settings must be a dictionary.'
        else:
            if 'voltage' not in custom_voltage:
                errors['custom_voltage.voltage'] = 'Voltage setting is required.'
            else:
                voltage = custom_voltage['voltage']
                if not isinstance(voltage, (int, float)) or voltage <= 0:
                    errors['custom_voltage.voltage'] = 'Voltage must be a positive number.'

            if 'tolerance' not in custom_voltage:
                errors['custom_voltage.tolerance'] = 'Tolerance setting is required.'
            else:
                tolerance = custom_voltage['tolerance']
                if not isinstance(tolerance, (int, float)) or tolerance <= 0:
                    errors['custom_voltage.tolerance'] = 'Tolerance must be a positive number.'

    return errors