from typing import Any, Dict

def validate_custom_voltage(
    data: Dict[str, Any], errors: Dict[str, str]
) -> Dict[str, str]:
    """
    Validate custom voltage settings.

    The function expects a key named 'custom_voltage' in the `data` dictionary.
    The value must be a numeric type (int or float) or a string that can be
    converted to a float. The voltage must be greater than 0 and less than or
    equal to 1000 (arbitrary upper bound). Any validation failures are
    recorded in the `errors` dictionary under the key 'custom_voltage'.

    Parameters
    ----------
    data : dict
        Dictionary containing the voltage value under the key 'custom_voltage'.
    errors : dict
        Dictionary to which error messages will be added.

    Returns
    -------
    dict
        The updated `errors` dictionary.
    """
    key = "custom_voltage"

    # Check presence
    if key not in data or data[key] is None:
        errors[key] = "Custom voltage is required."
        return errors

    value = data[key]

    # Try to interpret as a number
    try:
        # If it's a string, strip whitespace
        if isinstance(value, str):
            value_str = value.strip()
            if value_str == "":
                raise ValueError
            value_num = float(value_str)
        else:
            value_num = float(value)
    except (ValueError, TypeError):
        errors[key] = "Custom voltage must be a numeric value."
        return errors

    # Validate range
    if not (0 < value_num <= 1000):
        errors[key] = "Custom voltage must be between 0 and 1000."
        return errors

    # If everything is fine, no error is added
    return errors