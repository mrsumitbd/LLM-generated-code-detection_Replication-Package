class MmioAccess:
    """Single MMIO read or write operation."""
    
    def __init__(self, address, value=None, is_write=False, width=4):
        """
        Initialize an MMIO access operation.
        
        Args:
            address: Memory address for the operation
            value: Data value (required for writes, optional for reads)
            is_write: Boolean indicating if this is a write operation
            width: Width of access in bytes (default 4)
        """
        self.address = address
        self.value = value
        self.is_write = is_write
        self.width = width
    
    def __repr__(self):
        """Return string representation of MMIO access."""
        op_type = "WRITE" if self.is_write else "READ"
        if self.is_write:
            return f"MmioAccess({op_type} addr=0x{self.address:x} value=0x{self.value:x} width={self.width})"
        else:
            return f"MmioAccess({op_type} addr=0x{self.address:x} width={self.width})"
    
    def __eq__(self, other):
        """Check equality with another MmioAccess object."""
        if not isinstance(other, MmioAccess):
            return False
        return (self.address == other.address and 
                self.value == other.value and 
                self.is_write == other.is_write and 
                self.width == other.width)
    
    def __hash__(self):
        """Return hash of MMIO access."""
        return hash((self.address, self.value, self.is_write, self.width))
    
    @classmethod
    def read(cls, address, width=4):
        """Create a read operation."""
        return cls(address=address, value=None, is_write=False, width=width)
    
    @classmethod
    def write(cls, address, value, width=4):
        """Create a write operation."""
        return cls(address=address, value=value, is_write=True, width=width)
    
    def get_mask(self):
        """Get the mask for the access width."""
        return (1 << (self.width * 8)) - 1
    
    def is_aligned(self):
        """Check if address is aligned to width."""
        return self.address % self.width == 0