def split_mantissa_unit(obj):
    if isinstance(obj, Quantity):
        return obj.magnitude, obj.units
    else:
        return obj, None