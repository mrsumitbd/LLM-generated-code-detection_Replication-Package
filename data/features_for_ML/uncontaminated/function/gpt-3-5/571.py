def read_value(id: int, type: BondType, data: BufferedReader) -> BondValue:
    if type == BondType.INT:
        return BondValue(id, type, int.from_bytes(data.read(4), byteorder='little'))
    elif type == BondType.FLOAT:
        return BondValue(id, type, struct.unpack('f', data.read(4))[0])
    elif type == BondType.STRING:
        str_length = int.from_bytes(data.read(4), byteorder='little')
        return BondValue(id, type, data.read(str_length).decode('utf-8'))
    else:
        raise ValueError("Invalid BondType")