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
    from astropy.units import Quantity
    
    if isinstance(obj, Quantity):
        return obj.value, obj.unit
    else:
        raise TypeError(f"Expected a Quantity object, got {type(obj).__name__}")