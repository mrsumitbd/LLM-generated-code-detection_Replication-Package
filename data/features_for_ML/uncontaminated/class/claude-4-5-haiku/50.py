class VectorStoreConfig:
    """Configuration for vector store connection."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, 
                 password: str = None, username: str = None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.username = username

    @property
    def dsn(self) -> str:
        """Generate DSN (Data Source Name) for vector store connection."""
        if self.username and self.password:
            return f"redis://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"
        elif self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        else:
            return f"redis://{self.host}:{self.port}/{self.db}"