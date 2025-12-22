def split_mantissa_unit(obj):
    """
    Split a Quantity into its mantissa and unit.

    Parameters
    ----------
    obj : `object`
        The object to check.

    Returns
    -------
    mantissa : `float` or `array_like`
        The mantissa of the `obj`.
    unit : Unit
        The physical unit of the `obj`.
    """
    if hasattr(obj, 'magnitude') and hasattr(obj, 'unit'):
        return obj.magnitude, obj.unit
    else:
        raise TypeError("Input object must have 'magnitude' and 'unit' attributes.")