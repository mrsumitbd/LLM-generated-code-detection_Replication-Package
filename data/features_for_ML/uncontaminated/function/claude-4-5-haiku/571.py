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
    if type == BondType.BT_BOOL:
        return BondValue(id, type, bool(int.from_bytes(data.read(1), byteorder='little')))
    elif type == BondType.BT_UINT8:
        return BondValue(id, type, int.from_bytes(data.read(1), byteorder='little'))
    elif type == BondType.BT_INT8:
        return BondValue(id, type, int.from_bytes(data.read(1), byteorder='little', signed=True))
    elif type == BondType.BT_UINT16:
        return BondValue(id, type, int.from_bytes(data.read(2), byteorder='little'))
    elif type == BondType.BT_INT16:
        return BondValue(id, type, int.from_bytes(data.read(2), byteorder='little', signed=True))
    elif type == BondType.BT_UINT32:
        return BondValue(id, type, int.from_bytes(data.read(4), byteorder='little'))
    elif type == BondType.BT_INT32:
        return BondValue(id, type, int.from_bytes(data.read(4), byteorder='little', signed=True))
    elif type == BondType.BT_UINT64:
        return BondValue(id, type, int.from_bytes(data.read(8), byteorder='little'))
    elif type == BondType.BT_INT64:
        return BondValue(id, type, int.from_bytes(data.read(8), byteorder='little', signed=True))
    elif type == BondType.BT_FLOAT:
        return BondValue(id, type, struct.unpack('<f', data.read(4))[0])
    elif type == BondType.BT_DOUBLE:
        return BondValue(id, type, struct.unpack('<d', data.read(8))[0])
    elif type == BondType.BT_STRING:
        length = int.from_bytes(data.read(4), byteorder='little')
        return BondValue(id, type, data.read(length).decode('utf-8'))
    elif type == BondType.BT_LIST:
        element_type_byte = data.read(1)
        element_type = BondType(int.from_bytes(element_type_byte, byteorder='little'))
        length = int.from_bytes(data.read(4), byteorder='little')
        elements = [read_value(i, element_type, data) for i in range(length)]
        return BondValue(id, type, elements)
    else:
        raise ValueError(f"Unknown BondType: {type}")