import struct
from typing import BinaryIO

# The following imports assume that BondType and BondValue are defined elsewhere
# in the same package or are imported from the bond library.
try:
    from bond import BondType, BondValue
except Exception:
    # Fallback definitions for environments where the bond library is not available.
    # These are minimal stubs to allow the function to run; replace with real imports
    # in a proper Bond environment.
    class BondType:
        INT32 = 1
        INT64 = 2
        FLOAT = 3
        DOUBLE = 4
        BOOL = 5
        STRING = 6
        # Add other types as needed

    class BondValue:
        def __init__(self, id: int, type: int, value):
            self.id = id
            self.type = type
            self.value = value

        def __repr__(self):
            return f"BondValue(id={self.id}, type={self.type}, value={self.value!r})"


def _read_int32(data: BinaryIO) -> int:
    raw = data.read(4)
    if len(raw) != 4:
        raise EOFError("Unexpected end of data while reading INT32")
    return struct.unpack("<i", raw)[0]


def _read_int64(data: BinaryIO) -> int:
    raw = data.read(8)
    if len(raw) != 8:
        raise EOFError("Unexpected end of data while reading INT64")
    return struct.unpack("<q", raw)[0]


def _read_float(data: BinaryIO) -> float:
    raw = data.read(4)
    if len(raw) != 4:
        raise EOFError("Unexpected end of data while reading FLOAT")
    return struct.unpack("<f", raw)[0]


def _read_double(data: BinaryIO) -> float:
    raw = data.read(8)
    if len(raw) != 8:
        raise EOFError("Unexpected end of data while reading DOUBLE")
    return struct.unpack("<d", raw)[0]


def _read_bool(data: BinaryIO) -> bool:
    raw = data.read(1)
    if len(raw) != 1:
        raise EOFError("Unexpected end of data while reading BOOL")
    return struct.unpack("<?", raw)[0]


def _read_string(data: BinaryIO) -> str:
    # Strings are prefixed with a 4‑byte unsigned length
    raw_len = data.read(4)
    if len(raw_len) != 4:
        raise EOFError("Unexpected end of data while reading STRING length")
    length = struct.unpack("<I", raw_len)[0]
    raw_str = data.read(length)
    if len(raw_str) != length:
        raise EOFError("Unexpected end of data while reading STRING content")
    return raw_str.decode("utf-8")


def read_value(id: int, type: BondType, data: BinaryIO) -> BondValue:
    """
    Reads a value by creating a new value and matching by type.

    Args:
    - id: ID of value
    - type: Type of value to be created
    - data: Reader to get the data from

    Returns:
    - Newly created BondValue.
    """
    if type == BondType.INT32:
        value = _read_int32(data)
    elif type == BondType.INT64:
        value = _read_int64(data)
    elif type == BondType.FLOAT:
        value = _read_float(data)
    elif type == BondType.DOUBLE:
        value = _read_double(data)
    elif type == BondType.BOOL:
        value = _read_bool(data)
    elif type == BondType.STRING:
        value = _read_string(data)
    else:
        # For unknown or unsupported types, read raw bytes until a sentinel or
        # until the end of the stream. Here we simply read all remaining data.
        # This fallback can be adjusted based on the actual Bond protocol.
        value = data.read()
    return BondValue(id, type, value)