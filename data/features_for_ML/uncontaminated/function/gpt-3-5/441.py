def validate_custom_voltage(data: dict[str, Any], errors: dict[str, str]) -> dict[str, str]:
    if 'voltage' not in data:
        errors['voltage'] = 'Voltage setting is missing'
    elif not isinstance(data['voltage'], (int, float)):
        errors['voltage'] = 'Voltage must be a number'
    elif data['voltage'] < 0:
        errors['voltage'] = 'Voltage must be a non-negative number'
    
    return errors