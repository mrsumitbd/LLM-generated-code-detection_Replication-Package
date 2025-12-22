class MmioAccess:
    def __init__(self, address, data=None, read=True):
        self.address = address
        self.data = data
        self.read = read

    def perform_operation(self):
        if self.read:
            print(f"Reading from address {self.address}")
        else:
            print(f"Writing data {self.data} to address {self.address}")

# Example usage
mmio_read = MmioAccess(0x1000)
mmio_read.perform_operation()

mmio_write = MmioAccess(0x2000, data=0xABCD, read=False)
mmio_write.perform_operation()