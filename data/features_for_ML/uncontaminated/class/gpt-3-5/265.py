class Config:
    """SQLModel configuration."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        
    def set_database_url(self, database_url: str):
        self.database_url = database_url
        
    def get_database_url(self) -> str:
        return self.database_url