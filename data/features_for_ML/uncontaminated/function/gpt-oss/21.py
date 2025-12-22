import dolphin

def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    if not isinstance(console_address, int):
        raise TypeError("console_address must be an integer")
    if not isinstance(value, int):
        raise TypeError("value must be an integer")
    if not (0 <= value <= 0xFF):
        raise ValueError("value must be a byte (0-255)")

    dolphin.write_byte(console_address, value)