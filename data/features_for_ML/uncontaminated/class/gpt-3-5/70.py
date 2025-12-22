class StorageInfo:
    """Storage information structure."""
    
    def __init__(self, capacity, used_space):
        self.capacity = capacity
        self.used_space = used_space
        
    def get_free_space(self):
        return self.capacity - self.used_space
    
    def is_full(self):
        return self.used_space == self.capacity
    
    def __str__(self):
        return f"Capacity: {self.capacity} GB, Used Space: {self.used_space} GB"