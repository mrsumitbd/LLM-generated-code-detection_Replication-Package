def read_value(id: int, type: BondType, data: BufferedReader) -> BondValue:
    """
    Reads a value by creating a new value and matching by type.

    Args:
    - id: ID of value
    - type: Type of value to be created
    - data: Reader to get the data from

    Returns:
    - Newly created BondValue.
    """
    if type == BondType.FLOAT:
        value = data.read_float()
        return FloatBondValue(id, value)
    elif type == BondType.INT:
        value = data.read_int()
        return IntBondValue(id, value)
    elif type == BondType.STRING:
        value = data.read_string()
        return StringBondValue(id, value)
    elif type == BondType.BOOL:
        value = data.read_bool()
        return BoolBondValue(id, value)
    else:
        raise ValueError(f"Unsupported BondType: {type}")