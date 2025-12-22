import struct
import dolphin_memory_engine as dme

def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dme.write_bytes(console_address, struct.pack('B', value))