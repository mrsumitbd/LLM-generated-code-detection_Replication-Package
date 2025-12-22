class VectorStoreConfig:
    """Configuration for vector store connection."""

    def __init__(self, dsn: str):
        self._dsn = dsn

    @property
    def dsn(self) -> str:
        return self._dsn