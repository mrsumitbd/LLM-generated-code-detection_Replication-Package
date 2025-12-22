class StorageInfo:
    """Storage information structure."""

    def __init__(self, total_size, used_size, free_size):
        self.total_size = total_size
        self.used_size = used_size
        self.free_size = free_size

    def __str__(self):
        return f"Total: {self.total_size} bytes, Used: {self.used_size} bytes, Free: {self.free_size} bytes"

    def __repr__(self):
        return f"StorageInfo(total_size={self.total_size}, used_size={self.used_size}, free_size={self.free_size})"

    def __eq__(self, other):
        if not isinstance(other, StorageInfo):
            return False
        return (self.total_size == other.total_size and
                self.used_size == other.used_size and
                self.free_size == other.free_size)

    def __ne__(self, other):
        return not self.__eq__(other)