class ChunkDiff:
    """Represents differences between new and existing chunks for smart updates."""
    
    def __init__(self, chunk_id, diff_type, diff_data):
        self.chunk_id = chunk_id
        self.diff_type = diff_type
        self.diff_data = diff_data
        
    def get_chunk_id(self):
        return self.chunk_id
    
    def get_diff_type(self):
        return self.diff_type
    
    def get_diff_data(self):
        return self.diff_data