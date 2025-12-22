import dolphin_memory_engine

def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    assert isinstance(console_address, int)
    assert isinstance(value, int)

    dolphin_memory_engine.write_bytes(
        console_address, value.to_bytes(1, byteorder="big")
    )