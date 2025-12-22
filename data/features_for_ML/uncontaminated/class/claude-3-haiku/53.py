class MmioAccess:
    """Single MMIO read or write operation."""

    def __init__(self, address, value=None, size=4, is_write=False):
        self.address = address
        self.value = value
        self.size = size
        self.is_write = is_write

    def __str__(self):
        if self.is_write:
            return f"Write 0x{self.value:08X} to 0x{self.address:08X} ({self.size} bytes)"
        else:
            return f"Read from 0x{self.address:08X} ({self.size} bytes)"

    def __eq__(self, other):
        return (
            self.address == other.address
            and self.value == other.value
            and self.size == other.size
            and self.is_write == other.is_write
        )

    def __hash__(self):
        return hash((self.address, self.value, self.size, self.is_write))