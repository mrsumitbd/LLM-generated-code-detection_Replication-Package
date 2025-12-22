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
    # Try to import astropy's Quantity and Unit
    try:
        from astropy.units import Quantity, Unit
    except Exception:
        Quantity = None
        Unit = None

    # If astropy is available and obj is a Quantity, return its value and unit
    if Quantity is not None and isinstance(obj, Quantity):
        return obj.value, obj.unit

    # If pint is available and obj is a pint.Quantity, return its magnitude and units
    try:
        import pint
        if isinstance(obj, pint.Quantity):
            return obj.magnitude, obj.units
    except Exception:
        pass

    # If obj has 'value' and 'unit' attributes (generic), try to use them
    if hasattr(obj, "value") and hasattr(obj, "unit"):
        return getattr(obj, "value"), getattr(obj, "unit")

    # If obj is a tuple or list of (mantissa, unit)
    if isinstance(obj, (tuple, list)) and len(obj) == 2:
        mantissa, unit = obj
        return mantissa, unit

    # If obj is a scalar without unit, return it with None unit
    if isinstance(obj, (int, float, complex)):
        return float(obj), None

    # If obj is a numpy array without unit, return it with None unit
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj, None
    except Exception:
        pass

    # If none of the above, raise an error
    raise TypeError(
        f"Cannot split mantissa and unit from object of type {type(obj).__name__}. "
        "Expected an astropy Quantity, pint.Quantity, or an object with 'value' and 'unit' attributes."
    )