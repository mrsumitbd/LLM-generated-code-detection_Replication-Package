import struct
from typing import cast
from .madeleine import BondValue
from io import BufferedReader
from .uleb import uleb128_decode, sleb128_decode
from .bond_types import BondType

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
    val = BondValue(id, type, None)
    match type:
        case BondType.Struct:
            val.value = read_struct(data)
        case BondType.Int32 | BondType.Int64 | BondType.Int16:
            val.value = sleb128_decode(data)
        case BondType.Uint16 | BondType.Uint32 | BondType.Uint64:
            val.value = uleb128_decode(data)
        case BondType.Uint8:
            val.value = data.read(1)[0]
        case BondType.Int8:
            val.value = cast(int, struct.unpack("b", data.read(1))[0])
        case BondType.Bool:
            val.value = bool(data.read(1)[0])
        case BondType.Float:
            val.value = cast(float, struct.unpack("f", data.read(4))[0])
        case BondType.Double:
            val.value = cast(float, struct.unpack("d", data.read(8))[0])
        case BondType.Set | BondType.List:
            val.value = read_list(data, type)
        case BondType.Map:
            val.value = read_map(data)
        case BondType.Wstring:
            val.value = read_wstring(data)
        case BondType.String:
            val.value = read_string(data)
        case BondType.Stop | BondType.StopBase | BondType.Unavailable:
            ...
    return val