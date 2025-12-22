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
    obj = _to_quantity(obj)
    return obj.mantissa, obj.unit