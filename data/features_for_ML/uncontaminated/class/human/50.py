
class VectorStoreConfig:
    """Configuration for vector store connection."""

    host: str
    port: int
    database: str
    user: str
    password: str
    table_name: str
    embedding_dimension: int = 2048  # text-embedding-3-large dimension
    similarity_measure: str = "cosine"  # cosine, dot_product, euclidean

    @property
    def dsn(self) -> str:
        """Get PostgreSQL connection string."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"