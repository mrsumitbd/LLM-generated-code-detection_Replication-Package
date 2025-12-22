class MmioAccess:
    """Single MMIO read or write operation.

    Parameters
    ----------
    address : int
        The memory‑mapped address to access.
    size : int, optional
        Number of bytes to read or write (default 4).
    value : int, optional
        Value to write. For a read operation this is ``None`` until
        :meth:`execute` is called.
    is_write : bool, optional
        ``True`` for a write operation, ``False`` for a read
        (default ``False``).

    Notes
    -----
    The :meth:`execute` method expects a *memory map* object that
    behaves like a mutable ``bytes``/``bytearray`` slice.  For example
    a ``mmap.mmap`` instance or a ``bytearray`` can be used.

    Examples
    --------
    >>> mem = bytearray(16)
    >>> write = MmioAccess(4, size=2, value=0xABCD, is_write=True)
    >>> write.execute(mem)
    >>> read = MmioAccess(4, size=2)
    >>> read.execute(mem)
    43981
    """

    def __init__(self, address, size=4, value=None, is_write=False):
        if not isinstance(address, int) or address < 0:
            raise ValueError("address must be a non‑negative integer")
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")
        if is_write and value is None:
            raise ValueError("write operation requires a value")
        if not is_write and value is not None:
            raise ValueError("read operation should not have a value")

        self.address = address
        self.size = size
        self.value = value
        self.is_write = is_write

    def execute(self, mem_map):
        """Perform the MMIO operation on *mem_map*.

        Parameters
        ----------
        mem_map : mutable buffer
            An object supporting slice assignment and slicing
            (e.g. ``bytearray`` or ``mmap.mmap``).

        Returns
        -------
        int | None
            The read value for read operations, ``None`` for writes.
        """
        if self.is_write:
            data = self.value.to_bytes(self.size, byteorder="little", signed=False)
            mem_map[self.address : self.address + self.size] = data
            return None
        else:
            data = mem_map[self.address : self.address + self.size]
            self.value = int.from_bytes(data, byteorder="little", signed=False)
            return self.value

    def __repr__(self):
        op = "WRITE" if self.is_write else "READ"
        val = f"0x{self.value:X}" if self.value is not None else "None"
        return (
            f"<MmioAccess {op} addr=0x{self.address:X} "
            f"size={self.size} value={val}>"
        )

    def to_dict(self):
        """Return a dictionary representation of the access."""
        return {
            "address": self.address,
            "size": self.size,
            "value": self.value,
            "is_write": self.is_write,
        }